import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, useCallback } from "react";
import { filesApi } from "../api/endpoints";
import type { FileStatusResponse } from "../types";

export function useFileUpload() {
  const queryClient = useQueryClient();
  const [activeFileId, setActiveFileId] = useState<string | null>(null);

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const { data } = await filesApi.upload(file);
      return data;
    },
    onSuccess: (data) => {
      setActiveFileId(data.file_id);
    },
  });

  const processMutation = useMutation({
    mutationFn: async (fileId: string) => {
      const { data } = await filesApi.process(fileId);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });

  const statusQuery = useQuery({
    queryKey: ["fileStatus", activeFileId],
    queryFn: async (): Promise<FileStatusResponse> => {
      const { data } = await filesApi.getStatus(activeFileId!);
      return data;
    },
    enabled: !!activeFileId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === "processing" || status === "pending" ? 2000 : false;
    },
  });

  const uploadAndProcess = useCallback(
    async (file: File) => {
      const uploaded = await uploadMutation.mutateAsync(file);
      await processMutation.mutateAsync(uploaded.file_id);
    },
    [uploadMutation, processMutation]
  );

  const reset = useCallback(() => {
    setActiveFileId(null);
    uploadMutation.reset();
    processMutation.reset();
  }, [uploadMutation, processMutation]);

  return {
    uploadAndProcess,
    reset,
    isUploading: uploadMutation.isPending,
    isProcessing: processMutation.isPending,
    uploadError: uploadMutation.error,
    processError: processMutation.error,
    fileStatus: statusQuery.data,
    processResult: processMutation.data,
  };
}
