package main

import (
	/*
	"context"
	"fmt"
	"log"
	"time"

	"github.com/jackc/pgx/v5"
	*/
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
)

func main() {

	//dsn := "postgresql://ed:UKZw18mpJDVal8A9tKJNOQ@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&options=--cluster%3Dgolden-dingo-2123"
	//


	psqlInfo := fmt.Sprintf("host=192.168.1.10 port=5432 user=postgres password=terces## dbname=finance sslmode=disable")
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		panic(err)
	}

	fmt.Println("Successfully connected")
	sqlStmt := "SELECT vendor_number, vendor_short_desc FROM Finance.vendors WHERE vendor_short_desc ILIKE $1"
	var vendor_number int
	var vendor_short_desc string
	rows, err := db.Query(sqlStmt, "%wal%")
		if err != nil {
			panic(err)
		}
		defer rows.Close()
		for rows.Next() {
			err = rows.Scan(&vendor_number, &vendor_short_desc)
			if err != nil {
				panic(err)
			}
			fmt.Println(vendor_number, vendor_short_desc)
		}
		err = rows.Err()
		if err != nil {
			panic(err)
		}


	/*
	switch err := row.Scan(&vendor_number, &vendor_short_desc); err {
	case sql.ErrNoRows:
		fmt.Println("No rows returned")
	case nil:
		fmt.Println(vendor_number, vendor_short_desc)
	default:
		panic(err)
	}
	*/
	/*
	ctx := context.Background()
	conn, err := pgx.Connect(ctx, dsn)
	defer conn.Close(context.Background())
	if err != nil {
		log.Fatal("failed to connect database", err)
	}

	var now time.Time
	err = conn.QueryRow(ctx, "SELECT NOW()").Scan(&now)
	if err != nil {
		log.Fatal("failed to execute query", err)
	}

	fmt.Println(now)
	*/
}