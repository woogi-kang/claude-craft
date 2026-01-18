'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Sparkles } from 'lucide-react';

/**
 * Pricing Section - Glass Cards with Toggle
 *
 * Anti-AI-Slop:
 * ❌ NO identical pricing cards
 * ✅ Featured plan stands out visually
 * ✅ Interactive toggle with animation
 * ✅ Asymmetric highlighting
 */

const plans = [
  {
    name: 'Free',
    description: 'For individuals getting started',
    price: { monthly: 0, yearly: 0 },
    features: ['Up to 50 tasks', 'Basic AI suggestions', 'Mobile app', '1 project'],
    cta: 'Get Started',
    popular: false,
  },
  {
    name: 'Pro',
    description: 'For professionals who mean business',
    price: { monthly: 12, yearly: 9 },
    features: [
      'Unlimited tasks',
      'Advanced AI prioritization',
      'Calendar sync',
      'Unlimited projects',
      'Productivity analytics',
      'Priority support',
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Team',
    description: 'For teams that ship together',
    price: { monthly: 29, yearly: 24 },
    features: [
      'Everything in Pro',
      'Team workspaces',
      'Shared projects',
      'Admin controls',
      'SSO & security',
      'Dedicated success manager',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

export function Pricing() {
  const [isYearly, setIsYearly] = useState(true);

  return (
    <section className="py-32 relative">
      <div className="container mx-auto px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto mb-12"
        >
          <span
            className="text-sm font-bold uppercase tracking-widest text-accent mb-4 block"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Pricing
          </span>
          <h2
            className="text-4xl sm:text-5xl font-black tracking-tight mb-4"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Simple, transparent pricing.
          </h2>
          <p className="text-lg text-muted-foreground">
            Start free. Upgrade when you're ready.
          </p>
        </motion.div>

        {/* Billing Toggle */}
        <div className="flex items-center justify-center gap-4 mb-16">
          <span className={`text-sm font-medium ${!isYearly ? 'text-foreground' : 'text-muted-foreground'}`}>
            Monthly
          </span>
          <button
            onClick={() => setIsYearly(!isYearly)}
            className="relative w-16 h-8 rounded-full bg-muted p-1 transition-colors"
            style={{ backgroundColor: isYearly ? 'var(--color-primary)' : undefined }}
          >
            <motion.div
              layout
              className="w-6 h-6 rounded-full bg-white shadow-md"
              style={{ marginLeft: isYearly ? 'auto' : 0 }}
            />
          </button>
          <span className={`text-sm font-medium ${isYearly ? 'text-foreground' : 'text-muted-foreground'}`}>
            Yearly
            <span className="ml-2 px-2 py-0.5 bg-accent/20 text-accent text-xs font-bold rounded-full">
              Save 25%
            </span>
          </span>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className={`
                relative rounded-3xl p-8
                ${plan.popular
                  ? 'bg-gradient-to-br from-primary to-secondary text-white shadow-2xl shadow-primary/25 scale-105 z-10'
                  : 'glass'
                }
              `}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-highlight text-yellow-900 text-xs font-bold rounded-full flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Most Popular
                </div>
              )}

              {/* Plan Header */}
              <div className="mb-6">
                <h3
                  className="text-xl font-bold mb-2"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  {plan.name}
                </h3>
                <p className={`text-sm ${plan.popular ? 'text-white/80' : 'text-muted-foreground'}`}>
                  {plan.description}
                </p>
              </div>

              {/* Price */}
              <div className="mb-8">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={isYearly ? 'yearly' : 'monthly'}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="flex items-baseline gap-1"
                  >
                    <span className="text-5xl font-black" style={{ fontFamily: 'var(--font-display)' }}>
                      ${isYearly ? plan.price.yearly : plan.price.monthly}
                    </span>
                    <span className={`text-sm ${plan.popular ? 'text-white/60' : 'text-muted-foreground'}`}>
                      /month
                    </span>
                  </motion.div>
                </AnimatePresence>
                {isYearly && plan.price.monthly > 0 && (
                  <p className={`text-xs mt-1 ${plan.popular ? 'text-white/60' : 'text-muted-foreground'}`}>
                    Billed yearly (${plan.price.yearly * 12}/year)
                  </p>
                )}
              </div>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-sm">
                    <Check className={`w-5 h-5 shrink-0 ${plan.popular ? 'text-highlight' : 'text-accent'}`} />
                    <span className={plan.popular ? 'text-white/90' : ''}>{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`
                  w-full py-4 rounded-full font-semibold text-sm transition-colors
                  ${plan.popular
                    ? 'bg-white text-primary hover:bg-white/90'
                    : 'bg-foreground text-background hover:bg-foreground/90'
                  }
                `}
              >
                {plan.cta}
              </motion.button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
