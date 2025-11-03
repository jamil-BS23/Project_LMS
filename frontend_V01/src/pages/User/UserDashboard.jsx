

// src/pages/user/UserDashboard.jsx
import { useEffect, useState } from "react";
import UserSidebar from "../../components/UserSidebar/UserSidebar";
import axios from "axios";
import { parseISO, isBefore } from "date-fns";

export default function UserDashboard() {
  useEffect(() => {
    document.title = "My Library";
  }, []);

  const [myLoans, setMyLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [counts, setCounts] = useState({ borrowed: 0, overdue: 0, returned: 0 });

  const currentUserName = localStorage.getItem("username") || "User";

  const token = localStorage.getItem("token");
  if (!token) {
    setError("No token found. Please login.");
  }

  const headers = { Authorization: `Bearer ${token}` };

  const mapStatus = (loan) => {
    const today = new Date();
    const returnDate = loan.return_date ? parseISO(loan.return_date) : null;
    const status = loan.status;
    switch (status) {
      case "approved":
        if (returnDate && isBefore(returnDate, today)) return "Overdue";
        return "Borrowed";
      case "pending":
        return "Booked";
      case "returned":
        return "Returned";
      case "rejected":
        return "Rejected";
      default:
        return status;
    }
  };

  useEffect(() => {
    const fetchCountsAndLists = async () => {
      try {
        // Fetch counts
        const [borrowedRes, overdueRes, returnedRes] = await Promise.all([
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/borrow/status/accepted/count/my`, { headers }),
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/borrow/status/overdue/count/my`, { headers }),
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/borrow/status/returned/count/my`, { headers }),
        ]);

        setCounts({
          borrowed: borrowedRes.data.count,
          overdue: overdueRes.data.count,
          returned: returnedRes.data.count,
        });

        // Fetch lists
        const [borrowedListRes, overdueListRes] = await Promise.all([
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/borrow/status/accepted/list/my`, { headers }),
          axios.get(`${import.meta.env.VITE_API_BASE_URL}/borrow/status/overdue/list/my`, { headers }),
        ]);

        const combinedLoans = [
          ...borrowedListRes.data.map((loan) => ({ ...loan, status: "approved" })),
          ...overdueListRes.data.map((loan) => ({ ...loan, status: "approved" })),
        ];

        setMyLoans(combinedLoans);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load your loan data.");
      } finally {
        setLoading(false);
      }
    };

    fetchCountsAndLists();
  }, []);

  const statusBadge = (s) => {
    const base = "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium";
    if (s === "Overdue") return `${base} bg-red-100 text-red-700`;
    if (s === "Borrowed") return `${base} bg-sky-100 text-sky-700`;
    return `${base} bg-green-100 text-green-700`;
  };

  // ---------- Modal ----------
  const [modal, setModal] = useState({
    open: false,
    type: null,
    loan: null,
    date: "",
    note: "",
  });

  const openModal = (type, loan) =>
    setModal({ open: true, type, loan, date: loan?.due || "", note: "" });
  const closeModal = () =>
    setModal({ open: false, type: null, loan: null, date: "", note: "" });

  const [toast, setToast] = useState({ show: false, msg: "" });
  const showToast = (msg) => {
    setToast({ show: true, msg });
    setTimeout(() => setToast({ show: false, msg: "" }), 1800);
  };

  

  const returnLoan = async (loan) => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found - redirecting to login.");
      // optionally: navigate("/login");
      return;
    }
  
    // prepare headers
    const headers = {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  
    try {
      // PATCH endpoint expects status as a query param.
      // Use the same path format you've used elsewhere: /borrow/borrow/{id}/status
      const url = `${import.meta.env.VITE_API_BASE_URL}/borrow/${loan.borrow_id}/status`;
  
      // call PATCH with params (status=returned)
      const res = await axios.patch(url, null, {
        headers,
        params: { status: "returned" }, // <- important: matches FastAPI param
      });
  
      // If you want to inspect the response:
      // console.log("Patch response:", res);
  
      // Update UI: mark returned and set return_date
      setMyLoans((prev) =>
        prev.map((l) =>
          l.book_id === loan.book_id
            ? { ...l, status: "returned", return_date: new Date().toISOString() }
            : l
        )
      );
  
      showToast("Return recorded");
    } catch (err) {
      // Helpful debug information
      console.error("Failed to mark loan as returned:", err?.response ?? err?.message ?? err);
      // Provide user feedback
      showToast("Failed to record return. See console for details.");
    }
  };
  

  // const returnLoan = async (loan) => {
  //   try {
  //     await axios.put(
  //       `http://127.0.0.1:8000/borrows/${loan.id}/return`,
  //       {},
  //       { headers }
  //     );

  //     setMyLoans((prev) =>
  //       prev.map((l) =>
  //         l.id === loan.id
  //           ? { ...l, status: "returned", return_date: new Date().toISOString() }
  //           : l
  //       )
  //     );

  //     showToast("Return recorded");
  //   } catch (err) {
  //     console.error("Failed to return loan:", err);
  //   }
  // };

  const confirmModal = () => {
    if (modal.type === "expected") showToast("Expected date saved");
    else showToast("Return recorded");
    closeModal();
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      <UserSidebar active="dashboard" />
      <main className="flex-1 p-6 space-y-6">
        <h1 className="text-xl md:text-2xl font-bold text-gray-800">Welcome back!</h1>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-white rounded shadow p-4 text-center">
            <p className="text-sm text-gray-500">Borrowed</p>
            <p className="text-xl font-bold text-gray-800">{counts.borrowed}</p>
          </div>
          <div className="bg-white rounded shadow p-4 text-center">
            <p className="text-sm text-gray-500">Overdue</p>
            <p className="text-xl font-bold text-red-600">{counts.overdue}</p>
          </div>
          <div className="bg-white rounded shadow p-4 text-center">
            <p className="text-sm text-gray-500">Returned</p>
            <p className="text-xl font-bold text-gray-800">{counts.returned}</p>
          </div>
        </div>

        {/* My Loans */}
        <div className="bg-white rounded shadow">
          <div className="w-full overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left border-b border-gray-700">
                  <th className="py-2 px-3 text-gray-900">#</th>
                  <th className="py-2 px-3 min-w-[180px] text-gray-900">Title</th>
                  <th className="py-2 px-3 min-w-[160px] text-gray-900">User Name</th>
                  <th className="py-2 px-3 min-w-[140px] text-gray-900">Due Date</th>
                  <th className="py-2 px-3 min-w-[120px] text-gray-900">Status</th>
                  <th className="py-2 px-3 min-w-[220px] text-center text-gray-900">Action</th>
                </tr>
              </thead>

              <tbody>
                {myLoans.map((l, i) => (
                  <tr key={l.id} className="text-gray-900">
                    <td className="py-2 px-3">{i + 1}</td>
                    <td className="py-2 px-3 font-medium">{l.book_title}</td>
                    <td className="py-2 px-3">{l.user_name}</td>
                    <td className="py-2 px-3">
                      {l.return_date ? l.return_date.split("T")[0] : "-"}
                    </td>
                    <td className="py-2 px-3">
                      <span className={statusBadge(mapStatus(l))}>
                        {mapStatus(l)}
                      </span>
                    </td>
                    <td className="py-2 px-3 text-center">
                      <button
                        type="button"
                        onClick={() => returnLoan(l)}
                        className="inline-flex items-center gap-1 rounded-md bg-green-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400"
                      >
                        Return
                      </button>
                    </td>
                  </tr>
                ))}
                {myLoans.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-gray-500">
                      No active loans.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
