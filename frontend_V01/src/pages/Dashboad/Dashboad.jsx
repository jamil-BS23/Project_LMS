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

<<<<<<< HEAD
export default function Dashboard() {
  // ------------------------- TITLE -------------------------
=======
export const axiosAuth = () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("No token found. Please login.");

  return axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};





export default function Dashboard() {

  
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
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
<<<<<<< HEAD
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
=======

  // utils/axiosAuth.js
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const api = axiosAuth(); // use axios instance with token
  
        const [borrowedRes, returnedRes, pendingRes, totalRes] =
          await Promise.all([
            api.get("/borrow/status/accepted/count"),
            api.get("/borrow/status/returned/count"),
            api.get("/borrow/status/pending/count"),
            api.get("/books/count"),
          ]);
  
        const borrowed = borrowedRes.data.count || 0;
        const total = totalRes.data.count || 0;
  
        setStats({
          borrowed_copies: borrowed,
          returned_copies: returnedRes.data.count || 0,
          pending_copies: pendingRes.data.count || 0,
          total_copies: total,
          available_copies: total - borrowed,
        });
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
      } catch (err) {
        console.error("Error fetching stats:", err.response?.data || err);
        setError("Failed to load stats");
      } finally {
        setLoading(false);
      }
    };
  
    fetchStats();
  }, []);
<<<<<<< HEAD

=======
  
  
  
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
  const dashboardItems = [
    { label: "Borrowed Books", value: stats.borrowed_copies },
    { label: "Returned Books", value: stats.returned_copies },
    { label: "Borrows Pending", value: stats.pending_copies },
    { label: "Total Books", value: stats.total_copies },
    { label: "Available Books", value: stats.available_copies },
  ];

  // ------------------------- PENDING BORROWS -------------------------
  const [requests, setRequests] = useState([]);
<<<<<<< HEAD
  const [rows, setRows] = useState([]); // overdue rows
=======
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0

  useEffect(() => {
    const fetchPendingRequests = async () => {
      try {
<<<<<<< HEAD
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
=======
        const api = axiosAuth();
        const res = await api.get("/borrow/status/pending/list");
        setRequests(res.data || []);
      } catch (err) {
        console.error("Error fetching pending requests:", err.response?.data || err);
        setError("Failed to load borrow requests");
      } finally {
        setLoading(false);
      }
    };
  
    fetchPendingRequests();
  }, []);
  


  //  useEffect(() => {
  //   const fetchPendingRequests = async () => {
  //     try {
  //   const token = localStorage.getItem("token"); // get your JWT token
  //   if (!token) {
  //     throw new Error("No token found, please login");
  //   }

  //   const response = await axios.get("http://localhost:8000/borrows/pending", {
  //     headers: {
  //       Authorization: `Bearer ${token}`, // attach token here
  //     },
  //   });

  //   setRequests(response.data);
  // } catch (err) {
  //   console.error("Error fetching pending requests:", err);
  //   setError("Failed to load borrow requests");
  // } finally {
  //   setLoading(false);
  // }
  //   };

  //   fetchPendingRequests();
  // }, []);

  
  // Confirmation modal state
 
  // Toast (2s)
  const [toast, setToast] = useState({ show: false, type: "accept", message: "" });
  const showToast = (type, message) => {
    setToast({ show: true, type, message });
    setTimeout(() => setToast({ show: false, type, message: "" }), 2000);
  };

  /*const doConfirm = () => {
    const { type, index } = confirm;
    if (index > -1) {
      setRequests((prev) => prev.filter((_, i) => i !== index));
      showToast(type, type === "accept" ? "Request accepted" : "Request rejected");
    }
    closeConfirm();
  };*/


  const [confirm, setConfirm] = useState({
    open: false,
    type: null,
    index: -1,
    id: null,
  });

  // ✅ This must be inside the component
  const openConfirm = (type, index, borrow_id) => {
    setConfirm({ open: true, type, index, id: borrow_id });
  };

  const closeConfirm = () => {
    setConfirm({ open: false, type: null, index: -1, id: null });
  };
  
  const doConfirm = async () => {
    const { type, id } = confirm;
    if (!id) {
      console.error("No borrow_id found:", confirm);
      return;
    }
  
    try {
      const api = axiosAuth();
      const res = await api.patch(`/borrow/${id}/status`, null, {
        params: { status: type === "accept" ? "accepted" : "rejected" },
      });
      console.log("Borrow status updated:", res.data);
  
      // ✅ Optionally refresh the pending list after approval/rejection
      setRequests(prev => prev.filter(r => r.borrow_id !== id));
  
      showToast(type, type === "accept" ? "Request accepted" : "Request rejected");
    } catch (err) {
      console.error("Failed to update borrow status:", err.response?.data || err);
      showToast("error", "Failed to update borrow status");
    } finally {
      closeConfirm();
    }
  };
  

  // -------------------- WEEKLY LINE CHART --------------------
  const WEEK_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  // Keep your 3 series but name them Borrowed/Returned/Overdue (weekly base)
  const series = useMemo(
    () => [
      { name: "Borrowed", color: "stroke-sky-500",   dot: "fill-sky-500",   values: [20, 55, 62, 28, 24, 68, 64] },
      { name: "Returned", color: "stroke-amber-500", dot: "fill-amber-400", values: [48, 40, 30, 18, 22, 42, 58] },
      { name: "Overdue",  color: "stroke-rose-500",  dot: "fill-rose-500",  values: [10, 30, 55, 58, 26, 40, 88] },
    ],
    []
  );

  

   const [rows, setRows] = useState([]);
   useEffect(() => {
    const fetchOverdue = async () => {
      try {
        const api = axiosAuth();
        const res = await api.get("/borrow/status/overdue/list");
        setRows(res.data || []);
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
      } catch (err) {
        console.error("Failed to fetch overdue history:", err.response?.data || err);
      }
    };
<<<<<<< HEAD

    fetchPendingRequests();
    fetchBorrows();
=======
  
    fetchOverdue();
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
  }, []);
  
  

  // useEffect(() => {
  //   const fetchBorrows = async () => {
  //     try {
  //       const token = localStorage.getItem("token");
  //       const res = await axios.get("http://localhost:8000/borrows", {
  //         headers: { Authorization: `Bearer ${token}` },
  //       });

  //       const today = new Date();
  //       const overdue = (res.data || []).filter((r) => {
  //         if (!r.return_date) return false;
  //         const due = new Date(r.return_date);
  //         return !r.returned_at && due < today;
  //       });

  //       setRows(overdue);
  //     } catch (err) {
  //       console.error("Failed to fetch overdue history:", err);
  //     }
  //   };

  //   fetchBorrows();
  // }, []);

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
<<<<<<< HEAD
=======
     

      {/* Main */}
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
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

<<<<<<< HEAD
      </main>
=======
            {/* Chart centered */}
            <div className="w-full flex justify-center">
              <svg
                viewBox={`0 0 ${chartBox.w} ${chartBox.h}`}
                width="100%"
                height="220"
                className="max-w-full"
                aria-label="Weekly Dynamics Line Chart"
              >
                {/* grid lines */}
                {[0, 0.25, 0.5, 0.75, 1].map((t, i) => {
                  const y = chartBox.padY + t * (chartBox.h - chartBox.padY * 2);
                  return (
                    <line
                      key={i}
                      x1={chartBox.padX}
                      x2={chartBox.w - chartBox.padX}
                      y1={y}
                      y2={y}
                      className="stroke-gray-200"
                      strokeWidth="1"
                    />
                  );
                })}

                {/* baseline */}
                <line
                  x1={chartBox.padX}
                  x2={chartBox.w - chartBox.padX}
                  y1={chartBox.h - chartBox.padY}
                  y2={chartBox.h - chartBox.padY}
                  className="stroke-gray-300"
                  strokeWidth="1"
                />

                {/* x labels */}
                {WEEK_LABELS.map((w, i) => (
                  <text
                    key={w}
                    x={sx(i)}
                    y={chartBox.h - 6}
                    textAnchor="middle"
                    className="fill-gray-400"
                    style={{ fontSize: 10 }}
                  >
                    {w}
                  </text>
                ))}

                {/* animated lines + dots */}
                {paths.map((p, idx) => (
                  <g key={idx}>
                    <path
                      ref={(el) => (pathRefs.current[idx] = el)}
                      d={p.d}
                      className={`${p.color}`}
                      fill="none"
                      strokeWidth="3"
                      strokeLinecap="round"
                    />
                    {p.values.map((v, i) => (
                      <circle
                        key={i}
                        cx={sx(i)}
                        cy={sy(v)}
                        r="3.4"
                        className={`${p.dot} stroke-white`}
                        strokeWidth="1.2"
                      />
                    ))}
                  </g>
                ))}
              </svg>
            </div>

            {/* Weekly legend UNDER chart (three horizontal blocks) */}
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-6">
              {series.map((s) => (
                <div key={s.name} className="flex items-start gap-3">
                  <span
                    className={`mt-2 inline-block w-8 h-1.5 rounded-full ${s.color.replace(
                      "stroke",
                      "bg"
                    )}`}
                  />
                  <div>
                    <p className="font-semibold text-gray-800">{s.name}</p>
                    <p className="text-[11px] leading-4 text-gray-400">Mon – Sun</p>
                    <p className="text-[11px] leading-4 text-gray-400">7 pts</p>
                    <p className="text-[11px] leading-4 text-gray-400">Updated weekly</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* ---------------------- Overdue’s History (email centered with icon) ---------------------- */}
          <div className="bg-white rounded shadow p-4">
            <h3 className="font-semibold mb-2">Overdue’s History</h3>
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left border-b border-gray-200">
                  <th className="w-10">#</th>
                  <th className="w-25">Book name</th>
                  <th className="w-10">User name</th>
                  <th className="text-center">Email</th>
                  <th className="w-10">Returned Date</th>
                </tr>
              </thead>
              <tbody>
                {rows.length > 0 ? (
            rows.map((r, idx) => (
              <tr key={r.id} className="border-b border-gray-200">
                <td>{idx + 1}</td>
                <td className="font-semibold">{r.book_title?r.book_title : "—"}</td>
                <td>{r.user_name?r.user_name : "—"}</td>
                <td className="text-center">
                  <span className="inline-flex items-center justify-center gap-1 text-gray-700">
                    <Mail size={16} className="text-gray-500" />
                    <span>{r.user_email? r.user_email : "—"}</span>
                  </span>
                </td>
                <td className="text-red-600 font-medium">
                  {r.return_date ? r.return_date.split("T")[0] : "—"}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={5} className="text-center text-gray-500 py-4">
                 No overdue records found
              </td>
            </tr>
          )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Borrow Request (functional) */}
        <div className="bg-white rounded shadow p-4">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">Borrow Request</h3>
            {/* <Link to="#" className="text-xs text-green-600 hover:underline">
              View All
            </Link> */}
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left border-b border-gray-200">
                <th className="w-10">#</th>
                <th>Book name</th>
                <th>User name</th>
                <th>Borrowed Date</th>
                <th>Returned Date</th>
                <th className="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              {currentRows.map((r, i) => (
                <tr key={`${r.book}__${r.user}__${i}`} className="border-b border-gray-200">
                  <td>{startIndex + i + 1}</td>
                  <td className="font-medium">{r.book_title}</td>
                  <td>{r.user_name}</td>
                  <td>{r.borrow_date.split('T')[0]}</td>
                  <td>{r.return_date.split('T')[0]}</td>
                  <td className="text-center">
                    <div className="flex items-center justify-center gap-2">
                      <button
                        type="button"
                        onClick={() => openConfirm("accept", i, r.borrow_id)}
                        className="rounded-md bg-green-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400"
                      >
                        Accept
                      </button>
                      <button
                        type="button"
                        onClick={() => openConfirm("reject", i, r.borrow_id)}
                        className="rounded-md bg-red-500 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-400 focus:outline-none focus:ring-2 focus:ring-red-300"
                      >
                        Reject
                      </button>
                    </div>
                  </td>
                </tr>
              ))}

              {requests.length === 0 && (
                <tr>
                  <td colSpan={6} className="py-6 text-center text-gray-500">
                    No pending borrow requests.
                  </td>
                </tr>
              )}
            </tbody>
            {requests.length > rowsPerPage && (
        <tfoot>
          <tr>
            <td colSpan={6} className="py-4 text-center">
              <div className="flex justify-center items-center gap-4">
                <button
                  onClick={handlePrev}
                  disabled={currentPage === 1}
                  className={`px-3 py-1 rounded-md text-sm font-medium ${
                    currentPage === 1
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : "bg-sky-500 text-white hover:bg-sky-600"
                  }`}
                >
                  Prev
                </button>
                <span className="text-gray-600 text-sm">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  onClick={handleNext}
                  disabled={currentPage === totalPages}
                  className={`px-3 py-1 rounded-md text-sm font-medium ${
                    currentPage === totalPages
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : "bg-sky-500 text-white hover:bg-sky-600"
                  }`}
                >
                  Next
                </button>
              </div>
            </td>
          </tr>
        </tfoot>
      )}
          </table>
        </div>
      </main>

      {/* ---- Confirm Modal (Accept / Reject) ---- */}
      {confirm.open && (
        <div
          className="fixed inset-0 z-50"
          aria-modal="true"
          role="dialog"
          onClick={(e) => {
            if (e.target === e.currentTarget) closeConfirm();
          }}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/50 opacity-0 animate-[fadeIn_.2s_ease-out_forwards]" />
          {/* Panel */}
          <div className="absolute inset-0 flex items-center justify-center px-4">
            <div className="w-full max-w-md rounded-lg bg-white shadow-lg border border-gray-200 opacity-0 translate-y-2 animate-[popIn_.22s_ease-out_forwards]">
              <div className="px-6 py-5">
                <div className="flex items-start gap-3">
                  <div className="mt-0.5">
                    {confirm.type === "accept" ? (
                      <CheckCircle2 className="text-green-600" size={24} />
                    ) : (
                      <AlertTriangle className="text-amber-500" size={24} />
                    )}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">
                      {confirm.type === "accept"
                        ? "Accept this borrow request?"
                        : "Reject this borrow request?"}
                    </h3>
                    {confirm.index > -1 && (
                      <p className="mt-1 text-sm text-gray-600">
                        <span className="font-medium">
                          {requests[confirm.index]?.book_title}
                        </span>{" "}
                        — {requests[confirm.index]?.user_name}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              <div className="px-6 py-4 bg-white border-t border-gray-200 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={closeConfirm}
                  className="rounded-md px-4 py-2 text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={doConfirm}
                  className={`rounded-md px-4 py-2 text-sm font-semibold text-white ${
                    confirm.type === "accept"
                      ? "bg-green-600 hover:bg-green-500 focus:ring-2 focus:ring-green-400"
                      : "bg-red-600 hover:bg-red-500 focus:ring-2 focus:ring-red-400"
                  }`}
                >
                  {confirm.type === "accept" ? "Confirm" : "Reject"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ---- Toast (2s) ---- */}
      {toast.show && (
        <div className="fixed bottom-6 right-6 z-[60] pointer-events-none animate-[toastIn_.25s_ease-out]">
          <div className="pointer-events-auto flex items-start gap-3 rounded-xl bg-white shadow-lg ring-1 ring-black/5 px-4 py-3">
            <div className="mt-0.5">
              {toast.type === "accept" ? (
                <CheckCircle2 className="text-green-600" size={22} />
              ) : (
                <XCircle className="text-red-600" size={22} />
              )}
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-900">
                {toast.type === "accept" ? "Accepted" : "Rejected"}
              </p>
              <p className="text-xs text-gray-600">{toast.message}</p>
            </div>
          </div>
        </div>
      )}

      {/* animations */}
      <style>{`
        @keyframes fadeIn { to { opacity: 1 } }
        @keyframes popIn { to { opacity: 1; transform: translateY(0) } }
        @keyframes toastIn { from { opacity: 0; transform: translateY(8px) scale(.98) } to { opacity: 1; transform: translateY(0) scale(1) } }
      `}</style>
>>>>>>> ac9fbe620e321eae6450e2318702cf1200bffae0
    </div>
  );
}
