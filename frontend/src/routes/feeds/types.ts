export type Feed = {
  id: number;
  user_id: string;
  name: string;
  locations: string[];
  user_query: string;
  order: number;
  src_poliflw: boolean;
  src_openspending: boolean;
  src_openbesluitvorming: boolean;
  src_cvdr: boolean;
  sort: string;
  sort_order: string;
  date_start: string | null;
  date_end: string | null;
  read_counts: Record<string, number>;
};
