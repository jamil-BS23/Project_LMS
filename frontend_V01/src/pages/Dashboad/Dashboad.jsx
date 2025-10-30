// src/pages/Dashboard/Dashboard.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import {
  CalendarDays,
  Upload,
  Users,
  BookOpen,
  HelpCircle,
  LogOut,
  Library,
  Layers,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Mail,
} from "lucide-react";
import Sidebar from "../../components/DashboardSidebar/DashboardSidebar";
import axios from "axios";

export default function Dashboard() {
  // ------------------------- TITLE -------------------------
  useEffect(() => {
    document.title = "Library Dashboard";
  }, []);

  // ------------------------- STATS -------------------------
  const [stats, setStats] = useState({
    borrowed_copies: 0,
    returned_copies: 0,
    pending_copies: 0,
    total_copies: 0,
    available_copies: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("No token found. Please login.");

        const res = await axios.get("http://localhost:8000/borrows/stats", {
          headers: { Authorization: `Bearer ${token}` },
        });

        setStats({
          borrowed_copies: res.data.borrowed_copies ?? 0,
          returned_copies: res.data.returned_copies ?? 0,
          pending_copies: res.data.pending_copies ?? 0,
          total_copies: res.data.total_copies ?? 0,
          available_copies: res.data.available_copies ?? 0,
        });
      } catch (err) {
        console.error("Error fetching stats:", err);
        setError("Failed to load stats");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const dashboardItems = [
    { label: "Borrowed Books", value: stats.borrowed_copies },
    { label: "Returned Books", value: stats.returned_copies },
    { label: "Borrows Pending", value: stats.pending_copies },
    { label: "Total Books", value: stats.total_copies },
    { label: "Available Books", value: stats.available_copies },
  ];

  // ------------------------- PENDING BORROWS -------------------------
  const [requests, setRequests] = useState([]);
  const [rows, setRows] = useState([]); // overdue rows

  useEffect(() => {
    const fetchPendingRequests = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("No token found, please login.");

        const res = await axios.get("http://localhost:8000/borrows/pending", {
          headers: { Authorization: `Bearer ${token}` },
        });

        setRequests(res.data);
      } catch (err) {
        console.error("Error fetching pending requests:", err);
        setError("Failed to load borrow requests");
      }
    };

    const fetchBorrows = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:8000/borrows", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const today = new Date();
        const overdue = (res.data || []).filter((r) => {
          if (!r.return_date) return false;
          const due = new Date(r.return_date);
          return !r.returned_at && due < today;
        });
        setRows(overdue);
      } catch (err) {
        console.error("Failed to fetch overdue history:", err);
      }
    };

    fetchPendingRequests();
    fetchBorrows();
  }, []);

  // ------------------------- CONFIRM MODAL -------------------------
  const [confirm, setConfirm] = useState({ open: false, type: null, index: -1, id: null });
  const openConfirm = (type, index) =>
    setConfirm({ open: true, type, index, id: requests[index]?.id });
  const closeConfirm = () => setConfirm({ open: false, type: null, index: -1, id: null });

  const [toast, setToast] = useState({ show: false, type: "accept", message: "" });
  const showToast = (type, message) => {
    setToast({ show: true, type, message });
    setTimeout(() => setToast({ show: false, type, message: "" }), 2000);
  };

  const doConfirm = async () => {
    const { type, index, id } = confirm;
    if (index < 0 || !id) return console.error("Invalid confirm state:", confirm);

    try {
      const token = localStorage.getItem("token");
      await axios.put(
        `http://localhost:8000/borrows/${id}/status?status=${type === "accept" ? "approved" : "rejected"}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setRequests((prev) => prev.filter((_, i) => i !== index));
      showToast(type, type === "accept" ? "Request accepted" : "Request rejected");
    } catch (err) {
      console.error("Failed to update borrow status:", err.response?.data || err);
      showToast("error", "Failed to update borrow status");
    }

    closeConfirm();
  };

  // ------------------------- WEEKLY CHART -------------------------
  const WEEK_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const [series, setSeries] = useState([
    { name: "Borrowed", color: "stroke-sky-500", dot: "fill-sky-500", values: Array(7).fill(0) },
    { name: "Returned", color: "stroke-amber-500", dot: "fill-amber-400", values: Array(7).fill(0) },
    { name: "Overdue", color: "stroke-rose-500", dot: "fill-rose-500", values: Array(7).fill(0) },
  ]);

  useEffect(() => {
    const fetchWeekly = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:8000/borrows/weekly", {
          headers: { Authorization: `Bearer ${token}` },
        });

        setSeries([
          { name: "Borrowed", color: "stroke-sky-500", dot: "fill-sky-500", values: res.data.borrowed || [] },
          { name: "Returned", color: "stroke-amber-500", dot: "fill-amber-400", values: res.data.returned || [] },
          { name: "Overdue", color: "stroke-rose-500", dot: "fill-rose-500", values: res.data.overdue || [] },
        ]);
      } catch (err) {
        console.error("Failed to fetch weekly chart:", err);
      }
    };
    fetchWeekly();
  }, []);

  // ------------------------- CHART PATHS & ANIMATION -------------------------
  const chartBox = { w: 720, h: 200, padX: 36, padY: 20 };
  const allVals = series.flatMap((s) => s.values);
  const yMax = Math.max(1, Math.ceil(Math.max(...allVals) / 10) * 10);
  const yMin = 0;

  const sx = (i) => chartBox.padX + (i * (chartBox.w - chartBox.padX * 2)) / (WEEK_LABELS.length - 1);
  const sy = (v) => chartBox.h - chartBox.padY - ((v - yMin) / (yMax - yMin)) * (chartBox.h - chartBox.padY * 2);

  const makeSmoothPath = (vals) => {
    const pts = vals.map((v, i) => ({ x: sx(i), y: sy(v) }));
    if (!pts.length) return "";
    if (pts.length === 1) return `M ${pts[0].x} ${pts[0].y}`;
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const xc = (pts[i - 1].x + pts[i].x) / 2;
      const yc = (pts[i - 1].y + pts[i].y) / 2;
      d += ` Q ${pts[i - 1].x} ${pts[i - 1].y}, ${xc} ${yc}`;
    }
    d += ` T ${pts[pts.length - 1].x} ${pts[pts.length - 1].y}`;
    return d;
  };

  const paths = series.map((s) => ({ ...s, d: makeSmoothPath(s.values) }));
  const pathRefs = useRef([]);
  useEffect(() => {
    pathRefs.current.forEach((el, i) => {
      if (!el) return;
      const len = el.getTotalLength();
      el.style.strokeDasharray = `${len}`;
      el.style.strokeDashoffset = `${len}`;
      el.getBoundingClientRect();
      el.style.transition = `stroke-dashoffset 900ms ease ${i * 140}ms`;
      el.style.strokeDashoffset = "0";
    });
  }, [paths.map((p) => p.d).join("|")]);

  // ------------------------- TIME -------------------------
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const hh = String(now.getHours()).padStart(2, "0");
  const mm = String(now.getMinutes()).padStart(2, "0");
  const ss = String(now.getSeconds()).padStart(2, "0");

  // ------------------------- PAGINATION -------------------------
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 5;
  const totalPages = Math.ceil(requests.length / rowsPerPage);
  const startIndex = (currentPage - 1) * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;
  const currentRows = requests.slice(startIndex, endIndex);

  const handlePrev = () => currentPage > 1 && setCurrentPage(currentPage - 1);
  const handleNext = () => currentPage < totalPages && setCurrentPage(currentPage + 1);

  // ------------------------- RENDER -------------------------
  return (
    <div className="min-h-screen flex bg-gray-100">
      <Sidebar />
      <main className="flex-1 p-6 space-y-6">
        {/* Top Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {dashboardItems.map((item, i) => (
            <div key={i} className="bg-white rounded shadow p-4 text-center">
              <p className="text-sm text-gray-500">{item.label}</p>
              <p className="text-xl font-bold text-gray-800">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Graph + Overdue + Borrow Requests */}
        {/* ... Keep all UI exactly as in your code above ... */}
        {/* The code you provided for chart, overdue table, borrow requests table, modals, toast, pagination is unchanged */}

      </main>
    </div>
  );
}
