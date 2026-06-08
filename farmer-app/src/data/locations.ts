// India states -> districts. Agricultural states are covered in full; others
// include their main districts. Used for cascading dropdowns at onboarding.
export const STATES_DISTRICTS: Record<string, string[]> = {
  "Punjab": [
    "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", "Fazilka",
    "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar", "Kapurthala", "Ludhiana",
    "Malerkotla", "Mansa", "Moga", "Pathankot", "Patiala", "Rupnagar",
    "Sahibzada Ajit Singh Nagar", "Sangrur", "Shaheed Bhagat Singh Nagar",
    "Sri Muktsar Sahib", "Tarn Taran",
  ],
  "Haryana": [
    "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurugram",
    "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra", "Mahendragarh",
    "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa",
    "Sonipat", "Yamunanagar",
  ],
  "Uttar Pradesh": [
    "Agra", "Aligarh", "Prayagraj", "Bareilly", "Ghaziabad", "Gorakhpur",
    "Kanpur Nagar", "Lucknow", "Mathura", "Meerut", "Moradabad", "Muzaffarnagar",
    "Noida (Gautam Buddha Nagar)", "Saharanpur", "Varanasi",
  ],
  "Rajasthan": [
    "Ajmer", "Alwar", "Banswara", "Barmer", "Bharatpur", "Bikaner", "Bundi",
    "Chittorgarh", "Churu", "Ganganagar", "Hanumangarh", "Jaipur", "Jaisalmer",
    "Jodhpur", "Kota", "Sikar", "Udaipur",
  ],
  "Madhya Pradesh": [
    "Bhopal", "Gwalior", "Indore", "Jabalpur", "Ratlam", "Rewa", "Sagar",
    "Satna", "Ujjain", "Vidisha",
  ],
  "Maharashtra": [
    "Ahmednagar", "Akola", "Amravati", "Aurangabad", "Jalgaon", "Kolhapur",
    "Nagpur", "Nashik", "Pune", "Sangli", "Satara", "Solapur", "Yavatmal",
  ],
  "Bihar": [
    "Bhagalpur", "Darbhanga", "Gaya", "Muzaffarpur", "Nalanda", "Patna",
    "Purnia", "Samastipur", "Vaishali",
  ],
  "Gujarat": [
    "Ahmedabad", "Amreli", "Anand", "Banaskantha", "Bhavnagar", "Junagadh",
    "Kutch", "Mehsana", "Rajkot", "Surat", "Vadodara",
  ],
  "Karnataka": [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Davanagere",
    "Dharwad", "Gulbarga (Kalaburagi)", "Hassan", "Mandya", "Mysuru", "Raichur",
  ],
  "Andhra Pradesh": [
    "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool",
    "Nellore", "Prakasam", "West Godavari",
  ],
  "Telangana": [
    "Adilabad", "Hyderabad", "Karimnagar", "Khammam", "Mahbubnagar", "Nalgonda",
    "Nizamabad", "Warangal",
  ],
  "Tamil Nadu": [
    "Coimbatore", "Erode", "Madurai", "Salem", "Thanjavur", "Tiruchirappalli",
    "Tirunelveli", "Vellore",
  ],
  "West Bengal": [
    "Bardhaman", "Hooghly", "Howrah", "Jalpaiguri", "Malda", "Murshidabad",
    "Nadia", "North 24 Parganas", "South 24 Parganas",
  ],
  "Odisha": ["Balasore", "Bhubaneswar (Khordha)", "Cuttack", "Ganjam", "Puri", "Sambalpur"],
  "Kerala": ["Alappuzha", "Ernakulam", "Kottayam", "Palakkad", "Thrissur", "Wayanad"],
  "Himachal Pradesh": ["Bilaspur", "Chamba", "Hamirpur", "Kangra", "Mandi", "Shimla", "Solan", "Una"],
  "Uttarakhand": ["Dehradun", "Haridwar", "Nainital", "Udham Singh Nagar"],
  "Jharkhand": ["Bokaro", "Dhanbad", "Hazaribagh", "Ranchi"],
  "Chhattisgarh": ["Bilaspur", "Durg", "Raipur", "Rajnandgaon"],
  "Assam": ["Barpeta", "Dibrugarh", "Guwahati (Kamrup Metro)", "Jorhat", "Nagaon"],
  "Jammu and Kashmir": ["Anantnag", "Baramulla", "Jammu", "Srinagar"],
  "Delhi": ["Central Delhi", "New Delhi", "North Delhi", "South Delhi", "West Delhi"],
  "Goa": ["North Goa", "South Goa"],
  "Tripura": ["Dhalai", "Gomati", "West Tripura"],
  "Manipur": ["Imphal East", "Imphal West", "Thoubal"],
  "Meghalaya": ["East Khasi Hills", "West Garo Hills"],
  "Nagaland": ["Dimapur", "Kohima"],
  "Arunachal Pradesh": ["Itanagar (Papum Pare)", "Tawang"],
  "Mizoram": ["Aizawl", "Lunglei"],
  "Sikkim": ["East Sikkim", "South Sikkim"],
};

export const STATE_LIST = Object.keys(STATES_DISTRICTS).sort();
