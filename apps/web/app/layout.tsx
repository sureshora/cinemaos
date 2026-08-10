import "./globals.css";

export const metadata = {
  title: "CinemaOS",
  description: "Agentic Cinema production command center",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
