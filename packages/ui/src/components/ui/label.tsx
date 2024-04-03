"use client"

import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { cva, type VariantProps } from "class-variance-authority"
import type {ClassValue} from "clsx";
import { cn } from "@ui/lib/utils"

const labelVariants = cva(
  "ui-text-sm ui-font-medium ui-leading-none peer-disabled:ui-cursor-not-allowed peer-disabled:ui-opacity-70"
)

interface LabelProps {
  type?: "default" | "header" | "link"
}

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> &
    VariantProps<typeof labelVariants> & LabelProps
>(({ className, type, ...props }, ref) => {

  const typeToSize: Record<string, ClassValue> = {
    default: "",
    link: "ui-cursor-pointer",
    header: "ui-text-xl ui-font-bold ui-text-gray-800"
  } as const;

  return (<LabelPrimitive.Root
    className={cn(labelVariants(), typeToSize[type ?? "default"], className)}
    ref={ref}
    {...props}
  />)
})
Label.displayName = LabelPrimitive.Root.displayName

export { Label }
