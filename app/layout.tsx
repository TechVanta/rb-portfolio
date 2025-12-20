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
  title: "Ravi Bhalala | Cloud Engineer & DevOps Specialist | AWS | AI Generalist",
  description:
    "Personal portfolio of Ravi Bhalala - Cloud Engineer, DevOps Specialist, and AI Generalist based in Toronto, Canada. Passionate about AWS, Infrastructure as Code, and building impactful solutions.",
  keywords: [
    "Ravi Bhalala",
    "Cloud Engineer",
    "DevOps",
    "AWS",
    "Terraform",
    "Software Developer",
    "AI Generalist",
    "Toronto",
    "Canada",
  ],
  authors: [{ name: "Ravi Bhalala" }],
  openGraph: {
    title: "Ravi Bhalala | Cloud Engineer & DevOps Specialist | AWS | AI Generalist",
    description:
      "Cloud Engineer, DevOps Specialist, and AI Generalist based in Toronto, Canada. Expert in AWS, Terraform, and building scalable cloud solutions.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Ravi Bhalala | Cloud Engineer & DevOps Specialist | AWS | AI Generalist",
    description:
      "Cloud Engineer, DevOps Specialist, and AI Generalist based in Toronto, Canada. Expert in AWS, Terraform, and building scalable cloud solutions.",
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
