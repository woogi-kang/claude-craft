'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Zap } from 'lucide-react';

/**
 * CTA Section - Bold Visual Impact
 *
 * Design: Full-width gradient with glass overlay
 * Strong call to action with urgency
 */

export function CTA() {
  return (
    <section className="py-32 relative">
      <div className="container mx-auto px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-[2.5rem] bg-gradient-to-br from-primary via-secondary to-primary p-12 lg:p-20"
        >
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-10 left-10 w-40 h-40 border-2 border-white rounded-full" />
            <div className="absolute bottom-10 right-10 w-60 h-60 border-2 border-white rounded-full" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 border border-white rounded-full" />
          </div>

          {/* Content */}
          <div className="relative z-10 text-center text-white">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 rounded-full mb-8"
            >
              <Zap className="w-4 h-4" />
              <span className="text-sm font-medium">14-day free trial • No credit card required</span>
            </motion.div>

            <h2
              className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight mb-6 max-w-3xl mx-auto"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Ready to get your time back?
            </h2>

            <p className="text-xl text-white/80 max-w-xl mx-auto mb-10">
              Join 10,000+ professionals who stopped drowning in tasks and started actually doing them.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-primary font-bold rounded-full shadow-lg hover:shadow-xl transition-shadow"
              >
                Start Free Trial
                <ArrowRight className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 backdrop-blur font-semibold rounded-full border border-white/20 hover:bg-white/20 transition-colors"
              >
                Schedule a Demo
              </motion.button>
            </div>
          </div>

          {/* Floating Elements */}
          <motion.div
            animate={{ y: [0, -20, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
            className="absolute top-20 right-20 w-16 h-16 bg-white/10 backdrop-blur rounded-2xl hidden lg:block"
          />
          <motion.div
            animate={{ y: [0, 15, 0] }}
            transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
            className="absolute bottom-20 left-20 w-12 h-12 bg-white/10 backdrop-blur rounded-full hidden lg:block"
          />
        </motion.div>
      </div>
    </section>
  );
}
