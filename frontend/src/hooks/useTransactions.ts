import { useQuery } from "@tanstack/react-query";
import { transactionsApi } from "../api/endpoints";

export function useTransactions() {
  return useQuery({
    queryKey: ["transactions"],
    queryFn: async () => {
      const { data } = await transactionsApi.list();
      return data;
    },
    staleTime: 30_000,
  });
}
