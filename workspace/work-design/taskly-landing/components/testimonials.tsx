'use client';

import { motion } from 'framer-motion';
import { Star } from 'lucide-react';

/**
 * Testimonials Section - Staggered Cards
 *
 * Anti-AI-Slop:
 * ❌ NO identical testimonial cards in a row
 * ✅ Different card heights (masonry-like)
 * ✅ Pull quote styling
 * ✅ Varied visual weights
 */

const testimonials = [
  {
    quote: "Taskly literally changed how I work. I used to spend 30 minutes every morning planning my day. Now it's done for me.",
    author: 'Sarah Chen',
    role: 'Product Manager at Stripe',
    rating: 5,
    featured: true,
  },
  {
    quote: "The AI suggestions are scary accurate. It knows when I'm overloaded before I do.",
    author: 'Marcus Johnson',
    role: 'Freelance Designer',
    rating: 5,
    featured: false,
  },
  {
    quote: "Our team's productivity increased 40% in the first month. The shared project views are game-changing.",
    author: 'Emily Rodriguez',
    role: 'Engineering Lead at Notion',
    rating: 5,
    featured: false,
  },
  {
    quote: "Finally, a task app that adapts to me instead of making me adapt to it.",
    author: 'James Park',
    role: 'Startup Founder',
    rating: 5,
    featured: false,
  },
];

export function Testimonials() {
  return (
    <section className="py-32 relative overflow-hidden">
      {/* Background Accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-secondary/5 to-transparent" />

      <div className="container mx-auto px-6 lg:px-8 relative">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto mb-16"
        >
          <span
            className="text-sm font-bold uppercase tracking-widest text-secondary mb-4 block"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Loved by Teams
          </span>
          <h2
            className="text-4xl sm:text-5xl font-black tracking-tight"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Don't take our word for it.
          </h2>
        </motion.div>

        {/* Testimonials Grid - Asymmetric */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.author}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className={`
                glass rounded-3xl p-8
                ${testimonial.featured ? 'lg:col-span-2 lg:row-span-1' : ''}
                ${index === 1 ? 'lg:translate-y-8' : ''}
              `}
            >
              {/* Stars */}
              <div className="flex gap-1 mb-4">
                {Array.from({ length: testimonial.rating }).map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-highlight text-highlight" />
                ))}
              </div>

              {/* Quote */}
              <blockquote
                className={`mb-6 leading-relaxed ${
                  testimonial.featured ? 'text-xl lg:text-2xl font-medium' : 'text-lg'
                }`}
              >
                "{testimonial.quote}"
              </blockquote>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-secondary" />
                <div>
                  <p className="font-semibold" style={{ fontFamily: 'var(--font-display)' }}>
                    {testimonial.author}
                  </p>
                  <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Logos */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <p className="text-sm text-muted-foreground mb-8">Trusted by teams at</p>
          <div className="flex flex-wrap justify-center items-center gap-x-12 gap-y-6 opacity-50">
            {['Stripe', 'Notion', 'Figma', 'Linear', 'Vercel'].map((company) => (
              <span
                key={company}
                className="text-2xl font-black tracking-tight"
                style={{ fontFamily: 'var(--font-display)' }}
              >
                {company}
              </span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
