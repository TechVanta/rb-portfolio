"use client";

import Link from "next/link";
import { useState } from "react";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/career", label: "Career" },
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Contact" },
];

export default function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md dark:bg-zinc-950/80 border-b border-zinc-200 dark:border-zinc-800">
      <div className="max-w-6xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            href="/"
            className="text-xl font-bold tracking-tight text-zinc-900 dark:text-white hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
          >
            RB<span className="text-blue-600">.</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Link
              href="/contact"
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-zinc-900 rounded-full hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 transition-colors"
            >
              Let&apos;s Connect
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 text-zinc-600 dark:text-zinc-400"
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-zinc-200 dark:border-zinc-800">
            <div className="flex flex-col gap-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setIsMenuOpen(false)}
                  className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white transition-colors"
                >
                  {link.label}
                </Link>
              ))}
              <Link
                href="/contact"
                onClick={() => setIsMenuOpen(false)}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-zinc-900 rounded-full hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 transition-colors w-fit"
              >
                Let&apos;s Connect
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
