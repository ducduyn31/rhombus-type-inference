"use client"
import type {FC} from "react";
import {
  Button,
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow
} from "@repo/ui/components";
import {useInference} from "../../(api)/inference-context";

export const TypeDisplay: FC = () => {
  const currentState = useInference((state) => state.currentState);
  const result = useInference((state) => state.result);
  const reset = useInference((state) => state.reset);

  if (currentState !== "success") return null;

  return (
    <Table>
      <TableCaption>Inference Result</TableCaption>
      <TableHeader>
        <TableRow>
          {result ? Object.keys(result).map((key) => (
            <TableHead key={key}>{key}</TableHead>
          )) : null}
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          {result ? Object.values(result).map((value) => (
            <TableCell className="text-center" key={value}>{value}</TableCell>
          )) : null}
        </TableRow>
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={result ? Object.keys(result).length : 0}>
            <Button className="mt-5" onClick={reset}>Try Again</Button>
          </TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  )
}