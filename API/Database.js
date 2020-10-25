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
        conn.query("SELECT * FROM batched;", (err, res) => {
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

  }

  getDestinations(){

  }

  getTruck(origin)
  {

  }
}