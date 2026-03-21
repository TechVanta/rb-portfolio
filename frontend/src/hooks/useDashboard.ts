import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/endpoints";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const { data } = await dashboardApi.get();
      return data;
    },
    staleTime: 30_000,
  });
}
