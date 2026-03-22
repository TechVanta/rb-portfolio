import { useCallback, useState } from "react";
import { useFileUpload } from "../hooks/useFileUpload";

export default function FileUploader() {
  const [dragActive, setDragActive] = useState(false);
  const {
    uploadAndProcess,
    reset,
    isUploading,
    isProcessing,
    uploadError,
    processError,
    processResult,
  } = useFileUpload();

  const handleFile = useCallback(
    async (file: File) => {
      const validTypes = [
        "application/pdf",
        "text/csv",
        "application/vnd.ms-excel",
      ];
      if (!validTypes.includes(file.type)) {
        alert("Please upload a PDF or CSV file.");
        return;
      }
      await uploadAndProcess(file);
    },
    [uploadAndProcess]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragActive(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const isLoading = isUploading || isProcessing;
  const error = uploadError || processError;

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
          dragActive
            ? "border-primary-500 bg-primary-50"
            : "border-gray-300 bg-white hover:border-gray-400"
        }`}
      >
        {isLoading ? (
          <div className="space-y-3">
            <div className="animate-spin h-8 w-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto" />
            <p className="text-sm text-gray-600">
              {isUploading ? "Uploading file..." : "Processing transactions..."}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="text-4xl">📄</div>
            <p className="text-gray-600">
              Drag & drop your bank statement here, or{" "}
              <label className="text-primary-600 font-medium cursor-pointer hover:underline">
                browse
                <input
                  type="file"
                  accept=".pdf,.csv"
                  onChange={handleChange}
                  className="hidden"
                />
              </label>
            </p>
            <p className="text-xs text-gray-400">Supports PDF and CSV files (max 10MB)</p>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-700">
            {(error as Error).message || "An error occurred. Please try again."}
          </p>
        </div>
      )}

      {processResult && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-sm text-green-700">
            Successfully processed {processResult.transaction_count} transactions
            from {processResult.filename}.
          </p>
          <button
            onClick={reset}
            className="mt-2 text-sm text-green-600 font-medium hover:underline"
          >
            Upload another file
          </button>
        </div>
      )}
    </div>
  );
}
