import Image from "next/image";
import Link from "next/link";
import Navigation from "./components/Navigation";
import Footer from "./components/Footer";

// Passion/Interest Card Data
const passions = [
  {
    icon: "💻",
    title: "Technology",
    description:
      "Passionate about cutting-edge tech, gadgets, and building innovative solutions that make a difference.",
  },
  {
    icon: "📚",
    title: "Lifelong Learning",
    description:
      "Avid reader with a deep love for books on philosophy, business, self-improvement, and technology.",
  },
  {
    icon: "🏋️",
    title: "Health & Fitness",
    description:
      "Committed to physical wellness through regular gym sessions and maintaining a health-conscious lifestyle.",
  },
  {
    icon: "🤔",
    title: "Philosophy",
    description:
      "Fascinated by philosophical thinking, exploring life's big questions and applying wisdom to everyday decisions.",
  },
  {
    icon: "🚀",
    title: "Entrepreneurship",
    description:
      "Driven by the desire to create, innovate, and build ventures that solve real-world problems.",
  },
  {
    icon: "🤝",
    title: "Collaboration",
    description:
      "Believer in the power of teamwork and building meaningful professional relationships.",
  },
];

// Value Proposition Cards
const valueProps = [
  {
    audience: "Employers",
    title: "A Dedicated Professional",
    description:
      "Bringing technical excellence, continuous learning mindset, and a strong work ethic to every project. I deliver results that exceed expectations.",
    cta: "View My Experience",
    href: "/career",
    icon: (
      <svg
        className="w-8 h-8"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
        />
      </svg>
    ),
  },
  {
    audience: "Investors",
    title: "A Visionary Builder",
    description:
      "Combining technical expertise with business acumen to identify opportunities and create scalable solutions with strong market potential.",
    cta: "Explore My Vision",
    href: "/about",
    icon: (
      <svg
        className="w-8 h-8"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
        />
      </svg>
    ),
  },
  {
    audience: "Co-Founders",
    title: "A Reliable Partner",
    description:
      "Seeking like-minded individuals who share the passion for building something meaningful. Let's turn ambitious ideas into reality together.",
    cta: "Let's Connect",
    href: "/contact",
    icon: (
      <svg
        className="w-8 h-8"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
        />
      </svg>
    ),
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-zinc-950">
      <Navigation />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950" />
        <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-blue-100/50 to-transparent dark:from-blue-950/20 dark:to-transparent" />

        <div className="relative max-w-6xl mx-auto px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            {/* Text Content */}
            <div className="order-2 lg:order-1">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-medium mb-6">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-500 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
                </span>
                Open to Opportunities
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-zinc-900 dark:text-white leading-tight">
                Hi, I&apos;m{" "}
                <span className="bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 bg-clip-text text-transparent">
                  Ravi Bhalala
                </span>
              </h1>

              <p className="mt-6 text-lg sm:text-xl text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-xl">
                A passionate technologist, lifelong learner, and aspiring entrepreneur 
                dedicated to building impactful solutions and meaningful connections.
              </p>

              <p className="mt-4 text-base text-zinc-500 dark:text-zinc-500 leading-relaxed max-w-xl">
                I blend technical expertise with a philosophical mindset, believing that 
                great technology should enhance human potential. Whether it&apos;s code, 
                business, or personal growth — I approach everything with curiosity and dedication.
              </p>

              {/* CTA Buttons */}
              <div className="mt-8 flex flex-col sm:flex-row gap-4">
                <Link
                  href="/contact"
                  className="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-white bg-zinc-900 rounded-full hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all shadow-lg hover:shadow-xl"
                >
                  Get In Touch
                  <svg
                    className="ml-2 w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 8l4 4m0 0l-4 4m4-4H3"
                    />
                  </svg>
                </Link>
                <Link
                  href="/about"
                  className="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-zinc-700 bg-white border border-zinc-300 rounded-full hover:bg-zinc-50 dark:text-zinc-300 dark:bg-zinc-800 dark:border-zinc-700 dark:hover:bg-zinc-700 transition-all"
                >
                  Learn More About Me
                </Link>
              </div>

              {/* Quick Stats */}
              <div className="mt-12 flex gap-8">
                <div>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-white">
                    5+
                  </div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">
                    Years Experience
                  </div>
                </div>
                <div className="w-px bg-zinc-200 dark:bg-zinc-700" />
                <div>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-white">
                    10+
                  </div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">
                    Projects Delivered
                  </div>
                </div>
                <div className="w-px bg-zinc-200 dark:bg-zinc-700" />
                <div>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-white">
                    ∞
                  </div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">
                    Curiosity
                  </div>
                </div>
              </div>
            </div>

            {/* Profile Image */}
            <div className="order-1 lg:order-2 flex justify-center lg:justify-end">
              <div className="relative">
                {/* Decorative Elements */}
                <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full blur-2xl opacity-20 dark:opacity-30" />
                <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full opacity-50" />

                {/* Profile Image Container */}
                <div className="relative w-64 h-64 sm:w-80 sm:h-80 lg:w-96 lg:h-96 rounded-full overflow-hidden border-4 border-white dark:border-zinc-800 shadow-2xl">
                  <Image
                    src="/images/profile-picture.png"
                    alt="Ravi Bhalala"
                    fill
                    className="object-cover"
                    priority
                  />
                </div>

                {/* Floating Badge */}
                <div className="absolute -bottom-2 -right-2 bg-white dark:bg-zinc-800 rounded-2xl px-4 py-2 shadow-lg border border-zinc-100 dark:border-zinc-700">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">🇨🇦</span>
                    <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                      Based in Canada
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* What Drives Me Section */}
      <section className="py-20 lg:py-32 bg-zinc-50 dark:bg-zinc-900">
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 dark:text-white">
              What Drives Me
            </h2>
            <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
              Beyond code and business, these are the passions and principles that shape who I am
              and how I approach every aspect of life.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
            {passions.map((passion, index) => (
              <div
                key={index}
                className="group p-6 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 hover:border-blue-300 dark:hover:border-blue-700 transition-all hover:shadow-lg"
              >
                <div className="text-4xl mb-4">{passion.icon}</div>
                <h3 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
                  {passion.title}
                </h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed">
                  {passion.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Value Proposition Section */}
      <section className="py-20 lg:py-32 bg-white dark:bg-zinc-950">
        <div className="max-w-6xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 dark:text-white">
              How I Can Add Value
            </h2>
            <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
              Whether you&apos;re looking for a team member, an investment opportunity, 
              or a co-founder, I bring unique value to every partnership.
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {valueProps.map((prop, index) => (
              <div
                key={index}
                className="group relative p-8 bg-gradient-to-br from-zinc-50 to-white dark:from-zinc-900 dark:to-zinc-800 rounded-3xl border border-zinc-200 dark:border-zinc-700 hover:border-blue-300 dark:hover:border-blue-700 transition-all hover:shadow-xl"
              >
                <div className="flex items-center justify-between mb-6">
                  <span className="text-xs font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                    For {prop.audience}
                  </span>
                  <div className="text-zinc-400 dark:text-zinc-500 group-hover:text-blue-500 transition-colors">
                    {prop.icon}
                  </div>
                </div>

                <h3 className="text-xl font-bold text-zinc-900 dark:text-white mb-3">
                  {prop.title}
                </h3>

                <p className="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed mb-6">
                  {prop.description}
                </p>

                <Link
                  href={prop.href}
                  className="inline-flex items-center text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors"
                >
                  {prop.cta}
                  <svg
                    className="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Philosophy Quote Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 dark:from-black dark:via-zinc-900 dark:to-black relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }} />
        </div>

        <div className="relative max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <div className="text-6xl mb-8">💭</div>
          <blockquote className="text-2xl sm:text-3xl lg:text-4xl font-light text-white leading-relaxed italic">
            &ldquo;The only way to do great work is to love what you do. If you haven&apos;t found it yet, 
            keep looking. Don&apos;t settle.&rdquo;
          </blockquote>
          <div className="mt-8 text-zinc-400">
            — A philosophy I live by every day
          </div>

          <div className="mt-12">
            <Link
              href="/about"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-zinc-900 bg-white rounded-full hover:bg-zinc-100 transition-all shadow-lg hover:shadow-xl"
            >
              Discover My Story
              <svg
                className="ml-2 w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32 bg-white dark:bg-zinc-950">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 dark:text-white">
            Let&apos;s Build Something Great Together
          </h2>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            Whether you have a project in mind, an opportunity to discuss, or just want to connect —
            I&apos;d love to hear from you.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl"
            >
              Start a Conversation
            </Link>
            <a
              href="https://www.linkedin.com/in/ravi-bhalala-97440111a/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-zinc-700 bg-white border border-zinc-300 rounded-full hover:bg-zinc-50 dark:text-zinc-300 dark:bg-zinc-800 dark:border-zinc-700 dark:hover:bg-zinc-700 transition-all"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
              Connect on LinkedIn
            </a>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
