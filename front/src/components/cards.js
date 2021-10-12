import React, { useState, useEffect } from "react";
import axios from "axios";
import Card from "react-bootstrap/Card";
const Deals = (props) => {
  const [deals, setDeals] = useState([]);
  useEffect(() => {
    fetchDeals();
  }, [deals]);
  const fetchDeals = () => {
    axios
      .get("http://127.0.0.1:5000/"+props.type)
      .then((res) => {
        setDeals(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  return (
    <div>
      <div className="item-container">
        {deals.map((deal) => (
          <Card style={{ width: "18rem" }} key={deal.deal_id}>
            <Card.Body>
              <Card.Title>Deal: {deal.deal_id}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
              Buyer id :{deal.buyer_id}
              </Card.Subtitle>
            </Card.Body>
          </Card>
        ))}
      </div>
    </div>
  );
};
export default Deals;
