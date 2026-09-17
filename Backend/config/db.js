const mongoose = require('mongoose');
const dns = require('dns');

const connectDB = async () => {
  try {
    // Set fallback DNS servers (Google / Cloudflare) to prevent Windows DNS ECONNREFUSED on SRV records
    try {
      dns.setServers(['8.8.8.8', '1.1.1.1']);
    } catch (dnsErr) {
      // Ignore if restricted
    }

    const conn = await mongoose.connect(process.env.MONGODB_URI);

    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB;

