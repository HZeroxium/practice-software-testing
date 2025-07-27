/**
 * Tool Categories Data Structure
 *
 * This module contains the hierarchical tool categories structure
 * based on real hardware store classifications and industry standards.
 *
 * Structure:
 * - Main categories (root level)
 * - Subcategories with specific tools/products
 * - Realistic naming conventions
 *
 * @author Software Testing Team
 * @version 1.0.0
 */

// Main tool categories with hierarchical structure
const TOOL_CATEGORIES = {
  "Hand Tools": {
    description: "Manual tools operated without power",
    subcategories: {
      Hammers: [
        "Claw Hammers",
        "Ball Peen Hammers",
        "Sledge Hammers",
        "Framing Hammers",
        "Masonry Hammers",
      ],
      Screwdrivers: [
        "Phillips Screwdrivers",
        "Flathead Screwdrivers",
        "Torx Screwdrivers",
        "Precision Screwdrivers",
        "Ratcheting Screwdrivers",
      ],
      Wrenches: [
        "Combination Wrenches",
        "Adjustable Wrenches",
        "Pipe Wrenches",
        "Socket Wrenches",
        "Torque Wrenches",
      ],
      Pliers: [
        "Needle Nose Pliers",
        "Lineman Pliers",
        "Locking Pliers",
        "Wire Strippers",
        "Crimping Pliers",
      ],
    },
  },

  "Power Tools": {
    description: "Electric and battery-powered tools",
    subcategories: {
      Drills: [
        "Cordless Drills",
        "Hammer Drills",
        "Impact Drills",
        "Drill Presses",
      ],
      Saws: [
        "Circular Saws",
        "Miter Saws",
        "Table Saws",
        "Jig Saws",
        "Reciprocating Saws",
      ],
      Sanders: [
        "Orbital Sanders",
        "Belt Sanders",
        "Palm Sanders",
        "Detail Sanders",
      ],
      Grinders: [
        "Angle Grinders",
        "Bench Grinders",
        "Die Grinders",
        "Cut-off Tools",
      ],
    },
  },

  "Measuring Tools": {
    description: "Precision measurement and marking instruments",
    subcategories: {
      "Linear Measurement": [
        "Tape Measures",
        "Rulers",
        "Calipers",
        "Micrometers",
      ],
      "Angular Measurement": [
        "Squares",
        "Levels",
        "Protractors",
        "Angle Finders",
      ],
      "Marking Tools": [
        "Chalk Lines",
        "Marking Gauges",
        "Scribes",
        "Center Punches",
      ],
    },
  },

  "Safety Equipment": {
    description: "Personal protective equipment and safety gear",
    subcategories: {
      "Eye Protection": [
        "Safety Glasses",
        "Safety Goggles",
        "Face Shields",
        "Welding Helmets",
      ],
      "Hand Protection": [
        "Work Gloves",
        "Cut Resistant Gloves",
        "Chemical Resistant Gloves",
        "Heat Resistant Gloves",
      ],
      "Head Protection": ["Hard Hats", "Bump Caps", "Hair Nets"],
      "Hearing Protection": [
        "Ear Plugs",
        "Ear Muffs",
        "Electronic Hearing Protection",
      ],
    },
  },

  "Storage & Organization": {
    description: "Tool storage and workshop organization solutions",
    subcategories: {
      "Tool Storage": [
        "Tool Boxes",
        "Tool Chests",
        "Tool Cabinets",
        "Rolling Tool Chests",
      ],
      "Workshop Storage": [
        "Pegboards",
        "Tool Panels",
        "Wall Cabinets",
        "Storage Bins",
      ],
    },
  },
};

// Generate flat arrays for Mockaroo fields
const CATEGORY_NAMES = [];
const CATEGORY_SLUGS = [];
const SUBCATEGORY_NAMES = [];
const SUBCATEGORY_SLUGS = [];

// Populate arrays from the hierarchical structure
Object.keys(TOOL_CATEGORIES).forEach((categoryName) => {
  CATEGORY_NAMES.push(categoryName);
  CATEGORY_SLUGS.push(
    categoryName.toLowerCase().replace(/\s+/g, "-").replace(/&/g, "and")
  );

  const subcategories = TOOL_CATEGORIES[categoryName].subcategories;
  Object.keys(subcategories).forEach((subcategoryName) => {
    SUBCATEGORY_NAMES.push(subcategoryName);
    SUBCATEGORY_SLUGS.push(
      subcategoryName.toLowerCase().replace(/\s+/g, "-").replace(/&/g, "and")
    );

    // Add individual tools as potential subcategories
    subcategories[subcategoryName].forEach((toolName) => {
      SUBCATEGORY_NAMES.push(toolName);
      SUBCATEGORY_SLUGS.push(
        toolName.toLowerCase().replace(/\s+/g, "-").replace(/&/g, "and")
      );
    });
  });
});

// Export all the data structures
module.exports = {
  TOOL_CATEGORIES,
  CATEGORY_NAMES,
  CATEGORY_SLUGS,
  SUBCATEGORY_NAMES,
  SUBCATEGORY_SLUGS,

  // Utility functions
  getCategoryNames: () => CATEGORY_NAMES,
  getSubcategoryNames: () => SUBCATEGORY_NAMES,
  getAllCategoryNames: () => [...CATEGORY_NAMES, ...SUBCATEGORY_NAMES],
  getAllCategorySlugs: () => [...CATEGORY_SLUGS, ...SUBCATEGORY_SLUGS],

  // Get subcategories for a specific parent category
  getSubcategoriesFor: (parentCategory) => {
    if (TOOL_CATEGORIES[parentCategory]) {
      return Object.keys(TOOL_CATEGORIES[parentCategory].subcategories);
    }
    return [];
  },

  // Get all tools under a subcategory
  getToolsFor: (parentCategory, subcategory) => {
    if (
      TOOL_CATEGORIES[parentCategory] &&
      TOOL_CATEGORIES[parentCategory].subcategories[subcategory]
    ) {
      return TOOL_CATEGORIES[parentCategory].subcategories[subcategory];
    }
    return [];
  },
};
