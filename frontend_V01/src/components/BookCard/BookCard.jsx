// import { Star } from "lucide-react";
// import { Link } from "react-router-dom";

// export default function BookCard({ book }) {
//   const safe = (v, d = "") => (v === undefined || v === null ? d : v);

//   // ----- status -----
//   const getStatus = (b) => {
//     if (typeof b?.inStock === "boolean") return b.inStock ? "Available" : "Stock Out";
//     const s = (b?.status || "").toString().trim().toLowerCase();
//     if (s.includes("out")) return "Stock Out";
//     if (s.includes("upcoming") || s.includes("coming")) return "Upcoming";
//     return "Available";
//   };
//   const statusText = getStatus(book);
//   const statusColor =
//     statusText === "Stock Out"
//       ? "text-red-600"
//       : statusText === "Upcoming"
//       ? "text-amber-600"
//       : "text-green-600";

//   // rating (stars only, no count)
//   const rating = Number(book?.rating ?? 0);

//   return (
//     <div className="relative min-w-[220px] sm:min-w-[260px] snap-start group select-none">
//       {/* Cover image with lighter custom shadow */}
//       <img
//         src={safe(book?.coverImage, book?.image)}
//         alt={safe(book?.title, "Book cover")}
//         loading="lazy"
//         className="mx-auto h-52 w-auto object-contain rounded-md shadow-[0_4px_10px_rgba(0,0,0,0.08)] transition-transform duration-300 group-hover:scale-[1.03]"
//       />

//       {/* Body */}
//       <div className="px-1 pt-3 text-center">
//         <h3 className="text-sm font-semibold text-gray-900 line-clamp-2">
//           {safe(book?.title, "Untitled")}
//         </h3>
//         {book?.author && (
//           <p className="mt-0.5 text-xs text-gray-600">{book.author}</p>
//         )}

//         {/* Stars */}
//         <div className="mt-2 flex items-center justify-center gap-1">
//           {[...Array(5)].map((_, i) => (
//             <Star
//               key={i}
//               className={`w-4 h-4 ${
//                 i < Math.round(rating) ? "text-yellow-500 fill-yellow-500" : "text-gray-300"
//               }`}
//             />
//           ))}
//         </div>

//         {/* Status */}
//         <div className={`mt-2 text-xs font-medium ${statusColor}`}>
//           {statusText}
//         </div>
//       </div>

//       {/* Hover overlay with centered View Details */}
//       <div className="pointer-events-none absolute inset-0 bg-white/70 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
//         <Link
//           to={`/book/${book.id}`}
//           className="pointer-events-auto bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold px-5 py-2 rounded-md shadow-md"
//         >
//           View Details
//         </Link>
//       </div>
//     </div>
//   )
import { Star } from "lucide-react";
import { Link } from "react-router-dom";

export default function BookCard({ book, compact = false, onClick }) {
  const safe = (v, d = "") => (v === undefined || v === null ? d : v);

  // Determine book status
  const getStatus = (b) => {
    if (b.available_copies < 1) return "Stock Out";
    const s = (b?.status || "").toString().trim().toLowerCase();
    if (s.includes("out")) return "Stock Out";
    if (s.includes("upcoming") || s.includes("coming")) return "Upcoming";
    return "Available";
  };

  const statusText = getStatus(book);
  const statusColor =
    statusText === "Stock Out"
      ? "text-red-600"
      : statusText === "Upcoming"
      ? "text-amber-600"
      : "text-green-600";

  const rating = Number(book?.book_rating ?? 0);

  // Format long titles nicely
  const formatTitle = (t) => {
    const title = safe(t, "Untitled").toString().trim();
    const words = title.split(/\s+/);
    if (words.length <= 3) return title;
    const first = words.slice(0, 3).join(" ");
    const rest = words.slice(3).join(" ");
    return `${first}\n${rest}`;
  };

  // ✅ Robust cover image handling
  const getCoverImage = () => {
    const img = book.coverImage || book.book_image || book.book_photo || book.image;
    if (!img) return "/images/placeholder.png"; // fallback

    // Backend /media folder serve
    if (img.startsWith("/media/")) return `http://localhost:8000${img}`;

    // MinIO URL fix (development)
    if (img.startsWith("http://127.0.0.1:9000")) {
      return img.replace("127.0.0.1:9000", "localhost:9000");
    }

    // Any other full URL
    if (img.startsWith("http")) return img;

    return "/images/placeholder.png"; // default fallback
  };

  const handleImageError = (e) => {
    e.target.src = "/images/placeholder.png";
  };

  return (
    <div
      onClick={onClick}
      className="relative w-[200px] sm:w-[200px] snap-start group select-none flex-shrink-0 cursor-pointer"
    >
      <div className="mx-auto h-56 w-full flex items-center justify-center">
        <img
          src={getCoverImage()}
          alt={safe(book?.book_title, "Book cover")}
          loading="lazy"
          onError={handleImageError}
          className="h-full w-auto object-contain rounded-md drop-shadow-[0_14px_22px_rgba(0,0,0,0.06)] transition-transform duration-300 group-hover:scale-[1.03]"
        />
      </div>

      <div className="px-1 pt-3 text-center flex flex-col items-center min-h-[170px]">
        <h3 className="text-sm font-semibold text-gray-900 whitespace-pre-line line-clamp-2">
          {formatTitle(book?.book_title)}
        </h3>

        {book?.book_author && (
          <p className="mt-0.5 text-xs text-gray-600">{book.book_author}</p>
        )}

        {!compact && (
          <>
            <div className="mt-2 flex items-center justify-center gap-1">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.round(rating)
                      ? "text-yellow-500 fill-yellow-500"
                      : "text-gray-300"
                  }`}
                />
              ))}
            </div>

            <div className={`mt-2 text-xs font-medium ${statusColor}`}>
              {statusText}
            </div>

            <div className="mt-3">
              <Link
                to={`/book/${book.book_id || book.id}`}
                className="inline-block bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold px-5 py-2 rounded-md shadow-md"
              >
                View Details
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}


// // src/components/BookCard/BookCard.jsx
// import { useEffect, useRef, useState } from "react";
// import { MoreVertical } from "lucide-react";

// export default function BookCard({
//   book,
//   onClick,                 // e.g. () => navigate(`/book/${book.id}`)
//   onReadThisBook,          // e.g. () => navigate(`/book/${book.id}`)
//   variant = "row",         // "row" for horizontal scrollers, "grid" for lists
//   status,                  // optional; if not provided we derive from book.status/stock/title
//   size = "auto",           // NEW: "auto" | "scroller"  -> "scroller" locks to same width as Recommended/Popular
//   className = "",
// }) {
//   const [menuOpen, setMenuOpen] = useState(false);
//   const cardRef = useRef(null);
//   const menuRef = useRef(null);

//   // derive status same way your Home page does
//   const defaultGetStatus = (b) => {
//     const raw = (b?.status || b?.stock || "").toString().trim().toLowerCase();
//     if (raw === "available") return "Available";
//     if (raw === "stock out" || raw === "out of stock" || raw === "out") return "Stock Out";
//     if (raw === "upcoming" || raw === "coming soon") return "Upcoming";
//     if ((b?.title || "").toLowerCase().includes("empire")) return "Stock Out";
//     return "Available";
//   };
//   const finalStatus = status || defaultGetStatus(book);

//   const statusClasses = (s) => {
//     const v = (s || "").toLowerCase();
//     if (v === "available") return "text-green-600";
//     if (v === "stock out") return "text-red-500";
//     if (v === "upcoming") return "text-amber-600";
//     return "text-gray-600";
//   };

//   // close menu on outside click
//   useEffect(() => {
//     const onDoc = (e) => {
//       if (!menuOpen) return;
//       if (
//         cardRef.current &&
//         !cardRef.current.contains(e.target) &&
//         menuRef.current &&
//         !menuRef.current.contains(e.target)
//       ) {
//         setMenuOpen(false);
//       }
//     };
//     document.addEventListener("mousedown", onDoc);
//     return () => document.removeEventListener("mousedown", onDoc);
//   }, [menuOpen]);

//   // design tokens copied from your Home.jsx (Recommended/Popular cards)
//   const cardBase =
//     "group cursor-pointer border border-gray-300 bg-white shadow-sm hover:shadow-md transition-shadow duration-200 rounded-lg overflow-hidden focus:outline-none focus:ring-2 focus:ring-sky-500 relative";
//   const imgBase =
//     "w-full h-40 object-cover transition-transform duration-300 group-hover:scale-[1.02]";
//   const bodyBase = "border-t border-gray-200 p-4";
//   const rowClasses = "min-w-[240px] sm:min-w-[280px] snap-start";
//   const gridClasses = "w-full";

//   // NEW: lock to the exact same width as the scroller cards when requested
//   const sizeClasses = size === "scroller" ? "w-[240px] sm:w-[280px]" : "";

//   const containerClass =
//     `${cardBase} ${variant === "row" ? rowClasses : gridClasses} ${sizeClasses} ${className}`.trim();

//   const handleRead = (e) => {
//     e.stopPropagation();
//     setMenuOpen(false);
//     onReadThisBook?.();
//   };

//   return (
//     <div
//       ref={cardRef}
//       role="button"
//       tabIndex={0}
//       onClick={onClick}
//       onKeyDown={(e) => {
//         if (e.key === "Enter" || e.key === " ") {
//           e.preventDefault();
//           onClick?.();
//         }
//       }}
//       className={containerClass}
//     >
//       {/* Cover */}
//       <img src={book?.image} alt={book?.title} className={imgBase} />

//       {/* Body (top divider) */}
//       <div className={bodyBase}>
//         <h3 className="text-sm font-semibold text-gray-800 line-clamp-2">
//           {book?.title}
//         </h3>
//         <p className="mt-1 text-xs text-gray-500">
//           {book?.category || "Category"}
//         </p>

//         <div className="mt-4 flex items-center justify-between">
//           <span className={`text-xs font-medium ${statusClasses(finalStatus)}`}>
//             {finalStatus}
//           </span>

//           {/* 3-dot menu */}
//           <div className="relative">
//             <button
//               type="button"
//               className="p-1.5 hover:bg-gray-100 rounded"
//               aria-haspopup="menu"
//               aria-expanded={menuOpen}
//               aria-label="More options"
//               title="More options"
//               onClick={(e) => {
//                 e.stopPropagation();
//                 setMenuOpen((s) => !s);
//               }}
//             >
//               <MoreVertical className="h-4 w-4 text-gray-500" />
//             </button>

//             {menuOpen && (
//               <div
//                 ref={menuRef}
//                 role="menu"
//                 className="absolute right-0 mt-2 w-40 rounded-md border border-gray-200 bg-white shadow-lg z-10"
//                 onClick={(e) => e.stopPropagation()}
//               >
//                 <button
//                   className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50"
//                   onClick={handleRead}
//                 >
//                   Read this Book
//                 </button>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }