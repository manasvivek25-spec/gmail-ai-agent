import React from "react"
import { cn } from "@/lib/utils"

const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { 
    variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link" | "ai"
    size?: "default" | "sm" | "lg" | "icon"
  }
>(({ className, variant = "default", size = "default", ...props }, ref) => {
  const variants = {
    default: "bg-primary text-white hover:bg-primary/90 shadow",
    destructive: "bg-red-500 text-white hover:bg-red-500/90 shadow-sm",
    outline: "border border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900 shadow-sm",
    secondary: "bg-slate-100 text-slate-900 hover:bg-slate-100/80 shadow-sm",
    ghost: "hover:bg-slate-100 hover:text-slate-900",
    link: "text-primary underline-offset-4 hover:underline",
    ai: "bg-primary text-white hover:bg-primary/90 shadow-md shadow-primary/20",
  }
  
  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-9 rounded-md px-3",
    lg: "h-11 rounded-md px-8",
    icon: "h-10 w-10",
  }

  return (
    <button
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Button.displayName = "Button"

export { Button }
