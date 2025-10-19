// app/layout.tsx (or pages/_app.tsx depending on your setup)
import './globals.css'; // adjust the path if needed
import React from "react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
