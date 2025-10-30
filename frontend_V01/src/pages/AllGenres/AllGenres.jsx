// src/pages/AllGenres/AllGenres.jsx
// import { useNavigate, useLocation } from "react-router-dom";
// import { useState, useEffect } from "react";
// import Sidebar from "../../components/Sidebar/Sidebar";
// import BookCard from "../../components/BookCard/BookCard";
// import axios from "axios";

// const getStockStatus = (b) => {
//   const raw = b.available_book;
//   if (typeof raw === "number" && raw < 1) return "Stock Out";
//   const t = b.book_category?.toLowerCase() || "";
//   if (t.includes("out")) return "Stock Out";
//   if (t.includes("upcoming")) return "Upcoming";
//   return "Available";
// };

// export default function AllGenres() {
//   const navigate = useNavigate();
//   const location = useLocation();

//   const [allBooks, setAllBooks] = useState([]);
//   const [totalBooks, setTotalBooks] = useState(0);
//   const [totalPages, setTotalPages] = useState(1);
//   const [loading, setLoading] = useState(false);
//   const [filter, setFilter] = useState(location.state?.filter || null);
//   const [page, setPage] = useState(1);
//   const [searchTerm, setSearchTerm] = useState("");
//   const PAGE_SIZE = 9;

//   // 🔥 Fetch paginated books
//   const fetchBooks = async (pageNum = 1, currentFilter = filter, search = "") => {
//     try {
//       setLoading(true);

//       // Build query params for backend pagination
//       const params = new URLSearchParams();
//       params.append("page", pageNum);
//       params.append("size", PAGE_SIZE);
//       if (currentFilter?.type === "category") {
//         params.append("category", currentFilter.value);
//       }
//       if (search.trim()) {
//         params.append("search", search.trim());
//       }

//       const { data } = await axios.get(`http://localhost:8000/books/?${params.toString()}`);

//       // ✅ Handle paginated structure from backend
//       if (data && data.items) {
//         setAllBooks(data.items);
//         setTotalBooks(data.total || 0);
//         setTotalPages(data.pages || 1);
//       } else {
//         // fallback (in case backend returns array)
//         setAllBooks(Array.isArray(data) ? data : []);
//         setTotalBooks(data.length || 0);
//         setTotalPages(1);
//       }
//     } catch (err) {
//       console.error("Failed to fetch books:", err);
//       setAllBooks([]);
//       setTotalBooks(0);
//       setTotalPages(1);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 🕐 Debounce search input (waits 500ms)
//   useEffect(() => {
//     const handler = setTimeout(() => {
//       setPage(1);
//       fetchBooks(1, filter, searchTerm);
//     }, 500);
//     return () => clearTimeout(handler);
//   }, [searchTerm]);

//   // 🔁 Refetch on page or filter change
//   useEffect(() => {
//     fetchBooks(page, filter, searchTerm);
//   }, [filter, page]);

//   return (
//     <div className="flex min-h-screen bg-white">
//       {/* Sidebar */}
//       <Sidebar onSelect={setFilter} />

//       {/* Book Grid */}
//       <div className="flex-1 p-6">
//         <h1 className="text-2xl font-bold mb-6">All Genres</h1>

//         <div className="rounded-lg border border-gray-300 overflow-hidden bg-white">
//           <div className="px-4 py-3 bg-white">
//             <h2 className="text-lg sm:text-xl font-semibold text-gray-800">
//               Browse Books
//             </h2>
//           </div>

//           <div className="border-t border-gray-200">
//             {pageItems.length ? (
//               <div className="p-4">
//                 {/* EXACT 3-COLUMN GRID ON DESKTOP, SAME CARD SIZE AS SCROLLER */}
//                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6 justify-items-center">
//                   {pageItems.map((b) => (
//                     <BookCard
//                       key={b.id}
//                       book={{
//                         ...b,
//                         // coverImage: b.coverImage || b.image, // map to shared card field
//                         coverImage: b.image ? `http://localhost:8000${b.image}` : "",
//                         status: b.status || getStockStatus(b),
//                       }}
//                       variant="grid"
//                       size="scroller"
//                       status={b.status || getStockStatus(b)}
//                       onClick={() => goTo(b.id)}
//                       onReadThisBook={() => goTo(b.id)}
//                     />
//                   ))}
//                 </div>
//               </div>
//             ) : (
//               <div className="p-4 text-sm text-gray-500">No books found.</div>
//             )}

//             {/* Pagination (unchanged) */}
//             {filtered.length > 0 && totalPages > 1 && (
//               <div className="px-4 pb-4 flex items-center justify-between gap-2">
//                 <button
//                   onClick={() => setPage((p) => Math.max(1, p - 1))}
//                   disabled={page === 1}
//                   className={`px-3 py-1.5 text-sm rounded-md border border-gray-300 bg_white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed`}
//                 >
//                   Previous
//                 </button>

//                 <div className="flex items-center gap-1">
//                   {Array.from({ length: totalPages }, (_, i) => i + 1).map(
//                     (n) => (
//                       <button
//                         key={n}
//                         onClick={() => setPage(n)}
//                         className={`w-8 h-8 text-sm rounded-md border ${
//                           n === page
//                             ? "bg-sky-600 text-white border-sky-600"
//                             : "border-gray-300 bg-white hover:bg-gray-50"
//                         }`}
//                         aria-current={n === page ? "page" : undefined}
//                       >
//                         {n}
//                       </button>
//                     )
//                   )}
//                 </div>

//                 <button
//                   onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
//                   disabled={page === totalPages}
//                   className={`px-3 py-1.5 text-sm rounded-md border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed`}
//                 >
//                   Next
//                 </button>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }



// src/pages/AllGenres/AllGenres.jsx
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar/Sidebar";
import BookCard from "../../components/BookCard/BookCard";
import axios from "axios";
 
const getStockStatus = (b) => {
  const raw = b.available_book;
  if (typeof raw === "number" && raw < 1) return "Stock Out";
  const t = b.book_category?.toLowerCase() || "";
  if (t.includes("out")) return "Stock Out";
  if (t.includes("upcoming")) return "Upcoming";
  return "Available";
};
 
export default function AllGenres() {
  const navigate = useNavigate();
  const location = useLocation();
 
  const [allBooks, setAllBooks] = useState([]);
  const [totalBooks, setTotalBooks] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState(location.state?.filter || null);
  const [page, setPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const PAGE_SIZE = 9;
 
  // 🔥 Fetch paginated books
  const fetchBooks = async (pageNum = 1, currentFilter = filter, search = "") => {
    try {
      setLoading(true);
 
      // Build query params for backend pagination
      const params = new URLSearchParams();
      params.append("page", pageNum);
      params.append("size", PAGE_SIZE);
      if (currentFilter?.type === "category") {
        params.append("category", currentFilter.value);
      }
      if (search.trim()) {
        params.append("search", search.trim());
      }
 
      const { data } = await axios.get(`http://localhost:8000/books/?${params.toString()}`);
 
      // ✅ Handle paginated structure from backend
      if (data && data.items) {
        setAllBooks(data.items);
        setTotalBooks(data.total || 0);
        setTotalPages(data.pages || 1);
      } else {
        // fallback (in case backend returns array)
        setAllBooks(Array.isArray(data) ? data : []);
        setTotalBooks(data.length || 0);
        setTotalPages(1);
      }
    } catch (err) {
      console.error("Failed to fetch books:", err);
      setAllBooks([]);
      setTotalBooks(0);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };
 
  // 🕐 Debounce search input (waits 500ms)
  useEffect(() => {
    const handler = setTimeout(() => {
      setPage(1);
      fetchBooks(1, filter, searchTerm);
    }, 500);
    return () => clearTimeout(handler);
  }, [searchTerm]);
 
  // 🔁 Refetch on page or filter change
  useEffect(() => {
    fetchBooks(page, filter, searchTerm);
  }, [filter, page]);
 
  const goTo = (id) => navigate(`/book/${id}`);
 
  return (
    <div className="flex min-h-screen bg-white">
      {/* Sidebar */}
      <Sidebar onSelect={setFilter} />

      {/* Main Section */}
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-6">All Genres</h1>
 
        <div className="rounded-lg border border-gray-300 overflow-hidden bg-white">
          {/* Header + Search */}
          <div className="px-4 py-3 bg-white flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-800">
              Browse Books
            </h2>

            {/* 🔍 Search Bar */}
            <div className="relative w-full sm:w-64">
              <input
                type="text"
                placeholder="Search books..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-sky-500 focus:outline-none"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="absolute right-3 top-2.5 h-5 w-5 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M11 18a7 7 0 100-14 7 7 0 000 14z" />
              </svg>
            </div>
          </div>

          {/* Book Grid */}
          <div className="border-t border-gray-200">
            {loading ? (
              <div className="p-4 text-sm text-gray-500">Loading books...</div>
            ) : allBooks.length ? (
              <div className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 justify-items-center">
                  {allBooks.map((b) => (
                    <BookCard
                      key={b.book_id || b.id}
                      book={{
                        ...b,
                        coverImage: b.book_pic
                          ? `http://localhost:8000${b.book_pic}`
                          : "https://via.placeholder.com/150",
                        status: getStockStatus(b),
                      }}
                      variant="grid"
                      size="scroller"
                      status={getStockStatus(b)}
                      onClick={() => goTo(b.book_id || b.id)}
                      onReadThisBook={() => goTo(b.book_id || b.id)}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="p-4 text-sm text-gray-500">No books found.</div>
            )}

            {/* Pagination Controls */}
            {totalBooks > 0 && totalPages > 1 && (
              <div className="px-4 pb-4 flex items-center justify-center gap-2">
                {/* Previous Button */}
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-3 py-1.5 text-sm rounded-md border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>

                {/* Page Numbers (show only 3 around current page) */}
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter((n) => n >= page - 1 && n <= page + 1) // 👈 only 3 pages around current
                  .map((n) => (
                    <button
                      key={n}
                      onClick={() => setPage(n)}
                      className={`w-8 h-8 text-sm rounded-md border ${n === page
                          ? "bg-sky-600 text-white border-sky-600"
                          : "border-gray-300 bg-white hover:bg-gray-50"
                        }`}
                    >
                      {n}
                    </button>
                  ))}

                {/* Next Button */}
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-3 py-1.5 text-sm rounded-md border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}