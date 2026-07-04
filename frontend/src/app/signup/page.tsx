"use client";

import Link from "next/link";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { AuthCard } from "@/components/auth/auth-card";
import { useAppState } from "@/components/providers/app-state-provider";
import { AuthSignupValues, authSignupSchema } from "@/lib/validation";

export default function SignupPage() {
  const { registerUser, googleLogin } = useAppState();
  const [status, setStatus] = useState<{ type: "success" | "error"; message: string } | null>(null);

  const form = useForm<AuthSignupValues>({
    resolver: zodResolver(authSignupSchema),
    defaultValues: {
      fullName: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  return (
    <main className="grid min-h-screen place-items-center px-4 py-8">
      <AuthCard
        title="Create your Align account"
        subtitle="Use one unique email and a secure password"
        footerLabel="Already registered?"
        footerHref="/login"
        footerAction="Log in"
      >
        <form
          onSubmit={form.handleSubmit(async (values) => {
            const result = await registerUser({
              fullName: values.fullName,
              email: values.email,
              password: values.password,
            });
            setStatus({ type: result.ok ? "success" : "error", message: result.message });
            if (result.ok) form.reset();
          })}
          className="space-y-4"
        >
          <label className="block space-y-1 text-sm text-slate-300">
            Full Name
            <input {...form.register("fullName")} className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2" />
            {form.formState.errors.fullName ? <span className="text-xs text-rose-400">{form.formState.errors.fullName.message}</span> : null}
          </label>

          <label className="block space-y-1 text-sm text-slate-300">
            Email
            <input {...form.register("email")} className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2" />
            {form.formState.errors.email ? <span className="text-xs text-rose-400">{form.formState.errors.email.message}</span> : null}
          </label>

          <label className="block space-y-1 text-sm text-slate-300">
            Password
            <input
              type="password"
              {...form.register("password")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2"
            />
            {form.formState.errors.password ? <span className="text-xs text-rose-400">{form.formState.errors.password.message}</span> : null}
          </label>

          <label className="block space-y-1 text-sm text-slate-300">
            Confirm Password
            <input
              type="password"
              {...form.register("confirmPassword")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2"
            />
            {form.formState.errors.confirmPassword ? (
              <span className="text-xs text-rose-400">{form.formState.errors.confirmPassword.message}</span>
            ) : null}
          </label>

          {status ? (
            <p className={`text-sm ${status.type === "success" ? "text-emerald-300" : "text-rose-400"}`}>{status.message}</p>
          ) : null}

          <button type="submit" className="w-full rounded-lg bg-cyan-500 px-3 py-2 font-semibold text-slate-900 hover:bg-cyan-400">
            Sign Up
          </button>

          <button
            type="button"
            onClick={async () => {
              const result = await googleLogin();
              if (!result.ok) {
                setStatus({ type: "error", message: result.message });
              } else {
                // If we had useRouter, we'd redirect, or we can rely on state
                window.location.href = "/dashboard";
              }
            }}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-white px-3 py-2 font-semibold text-slate-900 hover:bg-slate-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" className="w-5 h-5">
              <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
              <path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691z"/>
              <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
              <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
            </svg>
            Sign up with Google
          </button>

          <Link href="/login" className="block text-center text-sm text-cyan-300 hover:text-cyan-200">
            Back to Login
          </Link>
        </form>
      </AuthCard>
    </main>
  );
}
