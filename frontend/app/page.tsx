"use client";

import { AppProvider, useApp } from "@/lib/store";
import Navbar from "@/components/Navbar";
import LandingPage from "@/components/LandingPage";
import DashboardPage from "@/components/DashboardPage";
import ChatPage from "@/components/ChatPage";
import BookingPage from "@/components/BookingPage";

function AppContent() {
  const { currentPage } = useApp();

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      {currentPage === "landing" && <LandingPage />}
      {currentPage === "dashboard" && <DashboardPage />}
      {currentPage === "chat" && <ChatPage />}
      {currentPage === "booking" && <BookingPage />}
    </div>
  );
}

export default function Page() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}
