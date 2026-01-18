'use client';

import { motion } from 'framer-motion';
import { Brain, Calendar, Bell, Zap, LineChart, Users } from 'lucide-react';

/**
 * Features Section - Bento Grid Layout
 *
 * Anti-AI-Slop:
 * ❌ NO identical 3-4 card grid
 * ✅ Asymmetric Bento layout
 * ✅ Different card sizes
 * ✅ Interactive hover states
 */

const features = [
  {
    icon: Brain,
    title: 'AI Prioritization',
    description: 'Our AI learns your work patterns and automatically prioritizes tasks based on deadlines, importance, and your energy levels.',
    color: 'bg-primary/10 text-primary',
    size: 'lg', // Large card
  },
  {
    icon: Calendar,
    title: 'Smart Scheduling',
    description: 'Automatically finds the best time slots for deep work.',
    color: 'bg-secondary/10 text-secondary',
    size: 'sm',
  },
  {
    icon: Bell,
    title: 'Context-Aware Reminders',
    description: 'Get reminded at the right moment, not just the right time.',
    color: 'bg-accent/10 text-accent',
    size: 'sm',
  },
  {
    icon: Zap,
    title: 'Quick Capture',
    description: 'Voice, text, email forwarding—capture tasks from anywhere in seconds.',
    color: 'bg-highlight/20 text-yellow-700',
    size: 'md',
  },
  {
    icon: LineChart,
    title: 'Productivity Insights',
    description: 'Weekly reports show your patterns and help you optimize.',
    color: 'bg-secondary/10 text-secondary',
    size: 'md',
  },
  {
    icon: Users,
    title: 'Team Sync',
    description: 'Share projects, delegate tasks, stay aligned.',
    color: 'bg-primary/10 text-primary',
    size: 'sm',
  },
];

export function Features() {
  return (
    <section className="py-32 relative">
      <div className="container mx-auto px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-2xl mb-16"
        >
          <span
            className="text-sm font-bold uppercase tracking-widest text-primary mb-4 block"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Features
          </span>
          <h2
            className="text-4xl sm:text-5xl font-black tracking-tight mb-6"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Everything you need.
            <br />
            <span className="text-muted-foreground">Nothing you don't.</span>
          </h2>
        </motion.div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 auto-rows-[200px]">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const isLarge = feature.size === 'lg';
            const isMedium = feature.size === 'md';

            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
                className={`
                  glass rounded-3xl p-6 flex flex-col cursor-default
                  ${isLarge ? 'md:col-span-2 md:row-span-2' : ''}
                  ${isMedium ? 'md:col-span-2 lg:col-span-2' : ''}
                `}
              >
                {/* Icon */}
                <div className={`w-12 h-12 rounded-2xl ${feature.color} flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6" />
                </div>

                {/* Content */}
                <h3
                  className={`font-bold mb-2 ${isLarge ? 'text-2xl' : 'text-lg'}`}
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  {feature.title}
                </h3>
                <p className={`text-muted-foreground leading-relaxed ${isLarge ? 'text-base' : 'text-sm'}`}>
                  {feature.description}
                </p>

                {/* Large card: extra visual */}
                {isLarge && (
                  <div className="mt-auto pt-6">
                    <div className="flex gap-2">
                      {['High', 'Medium', 'Low'].map((priority, i) => (
                        <span
                          key={priority}
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            i === 0
                              ? 'bg-primary/20 text-primary'
                              : i === 1
                              ? 'bg-highlight/30 text-yellow-700'
                              : 'bg-muted text-muted-foreground'
                          }`}
                        >
                          {priority}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
