import { Hero } from '@/components/hero';
import { Features } from '@/components/features';
import { Testimonials } from '@/components/testimonials';
import { Pricing } from '@/components/pricing';
import { CTA } from '@/components/cta';
import { Footer } from '@/components/footer';

/**
 * Taskly Landing Page
 *
 * Style: Grade-School Bold + Liquid Glass Hybrid
 * - Vibrant primary colors (Orange, Blue, Green)
 * - Glassmorphism cards
 * - Playful but professional
 *
 * Anti-AI-Slop:
 * ❌ NO Inter, Roboto, Poppins
 * ❌ NO Purple gradients on white
 * ❌ NO Generic card grids
 * ✅ Albert Sans + DM Sans
 * ✅ Orange + Blue accent
 * ✅ Asymmetric layouts
 */
export default function LandingPage() {
  return (
    <main className="relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 animated-gradient -z-10" />
      <div className="fixed inset-0 grain -z-10" />

      {/* Content */}
      <Hero />
      <Features />
      <Testimonials />
      <Pricing />
      <CTA />
      <Footer />
    </main>
  );
}
