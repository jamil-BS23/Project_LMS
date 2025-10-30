// Sidebar.jsx
import { useState, useEffect } from "react";
import { ChevronDown } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

const CAT_MAX_H = "max-h-72";             
const SUB_MAX_H = "max-h-44 md:max-h-52"; 

export default function Sidebar({ onSelect }) {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [categories, setCategories] = useState([]);
  const [expandedKey, setExpandedKey] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);
  const [activeSubcategory, setActiveSubcategory] = useState(null);
  const [toast, setToast] = useState({ open: false, text: "", to: "" });

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/categories/all`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          // normalize structure
          const normalized = data.map(c => ({
            category_title: c.category_title || c.name || "Unknown",
            subcategories: Array.isArray(c.subcategories) ? c.subcategories : []
          }));
          setCategories(normalized);
        } else {
          setCategories([]);
        }
      })
      .catch((err) => {
        console.error("Failed to fetch categories:", err);
        setCategories([]);
      });
  }, [token, navigate]);

  const toggleExpand = (category) => {
    if (expandedKey === category) {
      setExpandedKey(null);
    } else {
      setExpandedKey(category);
    }
  };

  const setFilter = (payload) => {
    if (onSelect) {
      onSelect(payload);
    } else {
      if (payload) {
        navigate("/all-genres", { state: { filter: payload } });
      }
    }
  };

  const toggleCategoryCheckbox = (catName) => {
    if (activeCategory === catName && !activeSubcategory) {
      setActiveCategory(null);
      setExpandedKey(null);
      setFilter(null);
    } else {
      setActiveCategory(catName);
      setFilter({ type: "category", value: catName });
      setExpandedKey(catName);
    }
  };

  const toggleSubcategoryCheckbox = (sub, parent) => {
    if (activeSubcategory === sub) {
      setActiveSubcategory(null);
      setFilter({ type: "category", value: parent });
    } else {
      setActiveSubcategory(sub);
      setFilter({ type: "subcategory", value: sub, parent });
    }
  };

  return (
    <aside className="hidden md:block w-64 bg-white p-4 border-r border-gray-200 sticky top-28 overflow-y-hidden space-y-6">
      {toast.open && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40">
          <div className="relative bg-white rounded-md shadow-lg px-6 py-4 text-gray-800">
            <button
              aria-label="Close"
              onClick={() => setToast({ open: false, text: "", to: "" })}
              className="absolute -top-2 -right-2 bg-white border border-gray-200 rounded-full w-6 h-6 leading-none grid place-items-center shadow"
            >
              ×
            </button>
            <div className="text-sm font-medium">{toast.text}</div>
            {toast.to && (
              <div className="mt-2 text-xs">
                <Link to={toast.to} className="text-sky-600 hover:text-sky-700 underline">
                  View results
                </Link>
              </div>
            )}
          </div>
        </div>
      )}

      <div>
        <h3 className="text-base font-semibold mb-2">Categories</h3>
        <div className={`overflow-y-auto ${CAT_MAX_H} pr-1`}>
          <ul className="space-y-1 mb-2">
            <li>
              <Link
                to="/all-genres"
                className="w-full text-left text-sm text-gray-700 px-2 py-2 rounded block hover:bg-sky-100 transition-all duration-200 font-medium"
              >
                All Genre
              </Link>
            </li>
          </ul>

          <ul className="space-y-1">
            {Array.isArray(categories) && categories.map((cat) => {
              const open = expandedKey === cat.category_title;
              const catChecked = activeCategory === cat.category_title && !activeSubcategory;

              return (
                <li key={cat.category_title}>
                  <div className="flex items-center justify-between px-2 py-2 rounded hover:bg-sky-50">
                    <label className="flex items-center gap-2 flex-1 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={catChecked}
                        onChange={() => toggleCategoryCheckbox(cat.category_title)}
                        className="h-4 w-4 rounded border-gray-300 text-sky-600 focus:ring-sky-500"
                      />
                      <span className={`text-sm ${catChecked ? "text-sky-700 font-medium" : "text-gray-700"}`}>
                        {cat.category_title}
                      </span>
                    </label>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleExpand(cat.category_title);
                      }}
                      aria-label={open ? "Collapse" : "Expand"}
                      className="p-1 rounded hover:bg-white/60"
                    >
                      <ChevronDown
                        size={16}
                        className={`transition-transform duration-200 ${open ? "rotate-180" : ""} text-gray-500`}
                      />
                    </button>
                  </div>

                  {open && (
                    <ul className={`ml-6 mt-1 pr-1 space-y-1 overflow-y-auto ${SUB_MAX_H}`}>
                      {Array.isArray(cat.subcategories) && cat.subcategories.map((sub) => {
                        const subChecked = activeSubcategory === sub;
                        return (
                          <li key={sub}>
                            <label className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-sky-50 cursor-pointer">
                              <input
                                type="checkbox"
                                checked={subChecked}
                                onChange={() => toggleSubcategoryCheckbox(sub, cat.category_title)}
                                className="h-4 w-4 rounded border-gray-300 text-sky-600 focus:ring-sky-500"
                              />
                              <span className={`text-sm ${subChecked ? "text-sky-700 font-medium" : "text-gray-600"}`}>
                                {sub}
                              </span>
                            </label>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      </div>

      {/* Footer Filter button */}
      <div className="pt-1">
        <button
          className="block mx-auto bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold rounded px-5 py-2"
        >
          Filter
        </button>
      </div>
    </aside>
  );
}