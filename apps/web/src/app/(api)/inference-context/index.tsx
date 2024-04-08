"use client"

import type {FC, PropsWithChildren} from "react";
import {createContext, useContext} from "react";
import type {StoreApi} from "zustand";
import {useStore} from "zustand";
import {inferStore} from "./store.ts";
import type {InferState} from "./types.ts";

type InferenceContextType = StoreApi<InferState>;

const InferenceContext = createContext<InferenceContextType | null>(null);

export const useInference = <U,>(selector: (state: InferState) => U): U  => {
  const context = useContext(InferenceContext);
  if (!context) {
    throw new Error("useInferenceContext must be used within a InferenceContextProvider");
  }
  return useStore<InferenceContextType, U>(context, selector);
}

export const InferenceContextProvider: FC<PropsWithChildren> = ({children}) => {
  return (
    <InferenceContext.Provider value={inferStore}>
      {children}
    </InferenceContext.Provider>
  )
}
