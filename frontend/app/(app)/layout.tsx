import { Sidebar } from '@/components/sidebar';

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-64 flex-shrink-0">
        <Sidebar />
      </aside>
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}