'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Play } from 'lucide-react';

/**
 * Hero Section - Grade-School Bold + Liquid Glass
 *
 * Design Decisions:
 * - Asymmetric layout (text left, visual right)
 * - Large, bold typography (Albert Sans)
 * - Floating glass cards with blur
 * - Playful geometric accents
 * - Orange primary CTA, Blue secondary
 */
export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-20 pb-32">
      <div className="container mx-auto px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left: Content */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="relative z-10"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8"
            >
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium">AI-Powered Task Management</span>
            </motion.div>

            {/* Headline */}
            <h1
              className="font-display text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.1] mb-6"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              <span className="block">Tasks that</span>
              <span className="block text-primary">organize</span>
              <span className="block">themselves.</span>
            </h1>

            {/* Subheadline */}
            <p className="text-xl text-muted-foreground max-w-lg mb-10 leading-relaxed">
              Stop drowning in to-dos. Taskly uses AI to prioritize, schedule,
              and remind you—so you can focus on what actually matters.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap gap-4">
              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center gap-2 px-8 py-4 bg-primary text-white font-semibold rounded-full shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-shadow"
              >
                Start Free Trial
                <ArrowRight className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center gap-2 px-8 py-4 glass rounded-full font-semibold hover:bg-white/80 transition-colors"
              >
                <Play className="w-5 h-5 text-secondary" />
                Watch Demo
              </motion.button>
            </div>

            {/* Social Proof */}
            <div className="mt-12 flex items-center gap-6">
              <div className="flex -space-x-3">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    className="w-10 h-10 rounded-full bg-gradient-to-br from-secondary to-accent border-2 border-white"
                  />
                ))}
              </div>
              <div className="text-sm">
                <span className="font-bold text-foreground">10,000+</span>
                <span className="text-muted-foreground"> professionals already organized</span>
              </div>
            </div>
          </motion.div>

          {/* Right: Visual */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="relative"
          >
            {/* Floating Cards */}
            <div className="relative h-[500px] lg:h-[600px]">
              {/* Main Card */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 glass rounded-3xl p-6 shadow-2xl"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                    <Sparkles className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-semibold">AI Suggestion</p>
                    <p className="text-sm text-muted-foreground">Just now</p>
                  </div>
                </div>
                <p className="text-sm leading-relaxed">
                  "Move <strong>Q4 Report</strong> to tomorrow. You have 3 meetings today
                  and this task needs deep focus."
                </p>
                <div className="mt-4 flex gap-2">
                  <button className="px-4 py-2 bg-primary text-white text-sm font-medium rounded-full">
                    Accept
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground">
                    Dismiss
                  </button>
                </div>
              </motion.div>

              {/* Task Card - Top Right */}
              <motion.div
                animate={{ y: [0, -15, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut', delay: 0.5 }}
                className="absolute top-10 right-0 w-64 glass rounded-2xl p-4 shadow-xl"
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 rounded bg-accent" />
                  <span className="text-sm font-medium">Design Review</span>
                </div>
                <div className="text-xs text-muted-foreground">Today, 2:00 PM</div>
                <div className="mt-3 h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full w-3/4 bg-accent rounded-full" />
                </div>
              </motion.div>

              {/* Stats Card - Bottom Left */}
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 3.5, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
                className="absolute bottom-10 left-0 w-48 glass rounded-2xl p-4 shadow-xl"
              >
                <p className="text-3xl font-black text-secondary">87%</p>
                <p className="text-sm text-muted-foreground">Tasks completed this week</p>
              </motion.div>

              {/* Decorative Elements */}
              <div className="absolute top-20 left-10 w-20 h-20 rounded-full bg-primary/20 blur-2xl" />
              <div className="absolute bottom-32 right-10 w-32 h-32 rounded-full bg-secondary/20 blur-3xl" />
              <div className="absolute top-1/2 right-20 w-16 h-16 rounded-full bg-highlight/30 blur-xl" />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Geometric Accents */}
      <div className="absolute top-40 left-10 w-4 h-4 bg-primary rounded rotate-45 opacity-60" />
      <div className="absolute bottom-40 right-20 w-6 h-6 bg-secondary rounded-full opacity-40" />
      <div className="absolute top-60 right-40 w-3 h-3 bg-accent opacity-50" />
    </section>
  );
}
