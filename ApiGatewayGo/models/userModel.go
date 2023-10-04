package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type User struct {
	ID        primitive.ObjectID `bson:"id"`
	FirstName *string            `json:"first_name"  validate:" required, min=2, max=28"`
	LastName  *string            `json:"last_name"  validate:" required, min=2, max=28"`
	Email     *string            `json:"email" validate:" email, required"`
	Password  *string            `json:"password" validate:"required, min=2"`
	CreatedAt time.Time          `bson:"created_at"`
	UpdatedAt time.Time          `bson:"updated_at"`
}
