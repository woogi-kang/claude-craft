import { LeftSidebar, StatusBar, ChatHistory, ChatConversation } from "@/components/layout";

export default function Home() {
  return (
    <div className="flex items-start h-screen w-full">
      {/* Left Sidebar - 300px fixed width */}
      <LeftSidebar />

      {/* Main Body - Flexible */}
      <div className="flex flex-1 flex-col h-full items-start min-h-px min-w-px overflow-hidden">
        {/* Status Bar - 80px height */}
        <StatusBar />

        {/* Main Content Area */}
        <div className="flex flex-1 items-start justify-between min-h-px min-w-px overflow-hidden w-full bg-[#FDFDFD]">
          {/* Chat Conversation Area - Flexible */}
          <ChatConversation />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
