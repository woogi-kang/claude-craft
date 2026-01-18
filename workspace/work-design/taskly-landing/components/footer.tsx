'use client';

import { motion } from 'framer-motion';
import { Twitter, Github, Linkedin, Mail } from 'lucide-react';

/**
 * Footer Section - Clean & Organized
 *
 * Simple 4-column layout with newsletter signup
 */

const footerLinks = {
  Product: ['Features', 'Pricing', 'Integrations', 'Changelog', 'Roadmap'],
  Company: ['About', 'Blog', 'Careers', 'Press', 'Contact'],
  Resources: ['Documentation', 'Help Center', 'API Reference', 'Status', 'Community'],
  Legal: ['Privacy', 'Terms', 'Security', 'Cookies'],
};

const socialLinks = [
  { icon: Twitter, href: '#', label: 'Twitter' },
  { icon: Github, href: '#', label: 'GitHub' },
  { icon: Linkedin, href: '#', label: 'LinkedIn' },
  { icon: Mail, href: '#', label: 'Email' },
];

export function Footer() {
  return (
    <footer className="border-t border-border/50 bg-muted/30">
      <div className="container mx-auto px-6 lg:px-8 py-16">
        {/* Top Section */}
        <div className="grid lg:grid-cols-5 gap-12 mb-16">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div
              className="text-2xl font-black tracking-tight mb-4"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              <span className="text-primary">Task</span>ly
            </div>
            <p className="text-muted-foreground max-w-xs mb-6">
              AI-powered task management that helps you focus on what matters most.
            </p>

            {/* Newsletter */}
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-2 rounded-full bg-background border border-border text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              />
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-2 bg-primary text-white text-sm font-medium rounded-full"
              >
                Subscribe
              </motion.button>
            </div>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4
                className="font-semibold mb-4 text-sm"
                style={{ fontFamily: 'var(--font-display)' }}
              >
                {category}
              </h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link}>
                    <a
                      href="#"
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Section */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-8 border-t border-border/50">
          <p className="text-sm text-muted-foreground">
            © 2026 Taskly. All rights reserved.
          </p>

          {/* Social Links */}
          <div className="flex items-center gap-4">
            {socialLinks.map((social) => {
              const Icon = social.icon;
              return (
                <motion.a
                  key={social.label}
                  href={social.href}
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-10 h-10 rounded-full bg-muted flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted/80 transition-colors"
                  aria-label={social.label}
                >
                  <Icon className="w-5 h-5" />
                </motion.a>
              );
            })}
          </div>
        </div>
      </div>
    </footer>
  );
}
