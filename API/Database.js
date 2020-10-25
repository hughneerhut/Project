const mysql = require("mysql");

class Database
{
  constructor(){
    this.auth = {
      host: "localhost",
      user: "root",
      password: "rootpass",
      database: "records"
    }

    this.conn = mysql.createConnection(this.auth);
    console.log("Hello");
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
            console.log(err);
          else
            console.log("Hello");
        });
      }).catch(err => {
        console.log(err);
        reject(err);
      });
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

export default Database;