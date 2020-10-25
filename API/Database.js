const mysql = require("mysql");

module.exports = class Database
{
  constructor(){
    this.auth = {
      host: "localhost",
      user: "root",
      password: "rootpass",
      database: "project"
    }

    this.conn = mysql.createConnection(this.auth);
  }

  open(){
    let conn = this.conn;
    return new Promise((resolve, reject) => {
      conn.connect(err => {
        if(err)
          reject(err);
        else
          resolve(conn);
      })
    });
  }

  close(){
    this.conn.end();
  }

  getOrders(){
    return new Promise((resolve, reject) => {
      this.open().then(conn => {
        conn.query("SELECT * FROM processed;", (err, res) => {
          if(err)
            reject(err);
          else
            resolve(res);
        });
      }).catch(err => 
        reject(err));
    });
  }

  getOrigins(){
    return new Promise((resolve, reject) => {
      this.open().then(conn => {
        conn.query("SELECT origin FROM batched WHERE pickupIndex = 1;", (err, res) => {
          if(err)
            reject(err);
          else
            resolve(res);
        });
      }).catch(err => 
        reject(err));
    });
  }

  getDestinations(){
    return new Promise((resolve, reject) => {
      this.open().then(conn => {
        conn.query("SELECT destination FROM batched GROUP BY destination;", (err, res) => {
          if(err)
            reject(err);
          else
            resolve(res);
        });
      }).catch(err => 
        reject(err));
    });
  }

  getTruck(origin, destination)
  {
    return new Promise((resolve, reject) => {
      this.open().then(conn => {
        conn.query("SELECT truckID FROM batched WHERE origin = " + origin + " AND destination = " + destination + ";", (err, res) => {
          if(err)
            reject(err);
          else if(res.length == 0)
            resolve();
          else
            conn.query("SELECT "
                          + "b.pickupIndex," 
                          + "p.* "
                      +"FROM "
                          + "processed p "
                      +"INNER JOIN batched b "
                          + "ON p.orderID = b.orderID "
                      +"WHERE "
                          + "b.truckID = " + res[0].truckID + " "
                      +"ORDER BY "
                          + "b.pickupIndex;",
            (err, res) => {
              if(err)
                reject(err)
              else
                resolve(res);
            })
        });
      }).catch(err => 
        reject(err));
    });
  }
}