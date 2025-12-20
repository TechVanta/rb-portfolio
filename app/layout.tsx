import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ravi Bhalala | Technologist, Entrepreneur & Lifelong Learner",
  description:
    "Personal portfolio of Ravi Bhalala - A passionate technologist, entrepreneur, and lifelong learner dedicated to building impactful solutions and meaningful connections.",
  keywords: [
    "Ravi Bhalala",
    "Software Developer",
    "Entrepreneur",
    "Technology",
    "Portfolio",
    "Canada",
  ],
  authors: [{ name: "Ravi Bhalala" }],
  openGraph: {
    title: "Ravi Bhalala | Technologist, Entrepreneur & Lifelong Learner",
    description:
      "Personal portfolio of Ravi Bhalala - A passionate technologist, entrepreneur, and lifelong learner.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Ravi Bhalala | Technologist, Entrepreneur & Lifelong Learner",
    description:
      "Personal portfolio of Ravi Bhalala - A passionate technologist, entrepreneur, and lifelong learner.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
