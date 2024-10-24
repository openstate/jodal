// While Tanstack Query supports Svelte 5, it does not track $state updates.
// This is a simple workaround while Svelte 5 support is being developed.
// Follow the PR here: https://github.com/TanStack/query/pull/6981
// Or the discussion here: https://github.com/TanStack/query/discussions/7413

import {
  createQuery as createQueryImpl,
  type CreateQueryOptions,
  type CreateQueryResult,
  type DefinedCreateQueryResult,
  type DefinedInitialDataOptions,
  type UndefinedInitialDataOptions,
} from '@tanstack/svelte-query';

import type { DefaultError, QueryClient, QueryKey } from '@tanstack/query-core';

import { readable } from 'svelte/store';

export function stateToReadable<T>(cb: () => T) {
  return readable(cb(), (set) => {
    const dispose = $effect.root(() => {
      $effect.pre(() => {
        set(cb());
      });
    });
    return () => dispose();
  });
}

type FunctionedParams<T> = () => T;

export function createQuery<
  TQueryFnData = unknown,
  TError = DefaultError,
  TData = TQueryFnData,
  TQueryKey extends QueryKey = QueryKey,
>(
  options: FunctionedParams<
    DefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey>
  >,
  queryClient?: QueryClient
): DefinedCreateQueryResult<TData, TError>;
export function createQuery<
  TQueryFnData = unknown,
  TError = DefaultError,
  TData = TQueryFnData,
  TQueryKey extends QueryKey = QueryKey,
>(
  options: FunctionedParams<
    UndefinedInitialDataOptions<TQueryFnData, TError, TData, TQueryKey>
  >,
  queryClient?: QueryClient
): CreateQueryResult<TData, TError>;
export function createQuery<
  TQueryFnData = unknown,
  TError = DefaultError,
  TData = TQueryFnData,
  TQueryKey extends QueryKey = QueryKey,
>(
  options: FunctionedParams<
    CreateQueryOptions<TQueryFnData, TError, TData, TQueryKey>
  >,
  queryClient?: QueryClient
): CreateQueryResult<TData, TError> {
  return createQueryImpl(stateToReadable(options), queryClient);
}
