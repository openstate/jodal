import type { allSources } from "$lib/sources";

export type ElasticResponse<TSource, THighlight = {}> = {
  _shards: {
    failed: number;
    skipped: number;
    successful: number;
    total: number;
  };
  aggregations: Record<
    "source" | "location",
    {
      buckets: { doc_count: number; key: string }[];
      doc_count_error_upper_bound: number;
      sum_other_doc_count: number;
    }
  >;
  hits: {
    hits: Array<
      {
        _id: string;
        _index: string;
        _score: number | null;
        _source: TSource;
        _type: string;
        sort: number[];
      } & ({} extends THighlight ? {} : { highlight?: THighlight })
    >;
    max_score: number | null;
    total: {
      relation: string;
      value: number;
    };
  };
  timed_out: boolean;
  took: number;
};

export type DocumentSource = {
  created: string;
  data: Record<string, unknown>;
  doc_url: string;
  id: string;
  identifier: string;
  location: string;
  location_name: string;
  modified: string;
  processed: string;
  published: string;
  source: string;
  title: string;
  type: string;
  url: string;
};

export type DocumentResponse = ElasticResponse<
  DocumentSource,
  { description: Array<string>; title?: Array<string> }
>;

export type LocationSource = {
  id: string;
  kind: string;
  name: string;
  source: string;
  sources: Array<{
    id: string;
    name: string;
    source: string;
  }>;
  type: string[] | string;
};

export type LocationResponse = ElasticResponse<LocationSource>;

export type FeedResponse = {
  id: number;
  public_id: string;
  user_id: string;
  query: string;
  name: string;
  locations: string[];
  sources: string[];
  binoas_feed_id: string;
  binoas_user_id: number;
  binoas_frequency: string | null;
};

export type AggregationsResponse = {
  [T in (typeof allSources)[number]["value"]]?: {
    total_documents: number;
    first_date: string;
    last_date: string;
    monthly_documents: Array<{
      doc_count: 10;
      key: number;
      key_as_string: string;
    }>;
  };
};
