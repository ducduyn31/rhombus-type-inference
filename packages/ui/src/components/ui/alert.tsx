import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@ui/lib/utils"

const alertVariants = cva(
  "ui-relative ui-w-full ui-rounded-lg ui-border ui-px-4 ui-py-3 ui-text-sm [&>svg+div]:ui-translate-y-[-3px] [&>svg]:ui-absolute [&>svg]:ui-left-4 [&>svg]:ui-top-4 [&>svg]:ui-text-foreground [&>svg~*]:ui-pl-7",
  {
    variants: {
      variant: {
        default: "ui-bg-background ui-text-foreground",
        destructive:
          "ui-border-destructive/50 ui-text-destructive dark:ui-border-destructive [&>svg]:ui-text-destructive",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
))
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("ui-mb-1 ui-font-medium ui-leading-none ui-tracking-tight", className)}
    {...props}
  />
))
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("ui-text-sm [&_p]:ui-leading-relaxed", className)}
    {...props}
  />
))
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }
