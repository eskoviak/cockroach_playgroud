package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/jackc/pgx/v5"
)

func main() {

	dsn := "postgresql://ed:UKZw18mpJDVal8A9tKJNOQ@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/budget?sslmode=verify-full&options=--cluster%3Dgolden-dingo-2123"
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
}