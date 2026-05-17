import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "TalentScale AI",
  description: "AI Workforce Planning Assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}