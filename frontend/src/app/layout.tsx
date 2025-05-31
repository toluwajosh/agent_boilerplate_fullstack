import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Agent App',
  description: 'A boilerplate AI agent application with chat functionality',
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body className="min-h-screen bg-gray-100 font-sans antialiased">
        <main className="h-screen">
          {children}
        </main>
      </body>
    </html>
  );
} 