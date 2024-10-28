export type ElasticSearchResponse = {
  _shards: {
    failed: number;
    skipped: number;
    successful: number;
    total: number;
  };
  aggregations: {
    location: {
      buckets: unknown[];
      doc_count_error_upper_bound: number;
      sum_other_doc_count: number;
    };
    source: {
      buckets: unknown[];
      doc_count_error_upper_bound: number;
      sum_other_doc_count: number;
    };
  };
  hits: {
    hits: Array<{
      _id: string;
      _index: string;
      _score: number | null;
      _source: {
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
      _type: string;
      highlight: {
        description: string[];
      };
      sort: number[];
    }>;
    max_score: number | null;
    total: {
      relation: string;
      value: number;
    };
  };
  timed_out: boolean;
  took: number;
};
