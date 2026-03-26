import { Router, Request, Response } from 'express';

export const ordersRouter = Router();

interface Order {
  id: string;
  customerId: string;
  items: { productId: string; quantity: number; price: number }[];
  status: 'pending' | 'processing' | 'shipped' | 'delivered';
  createdAt: string;
}

const orders: Order[] = [
  {
    id: 'ord-001',
    customerId: 'cust-42',
    items: [
      { productId: 'prod-101', quantity: 2, price: 29.99 },
      { productId: 'prod-205', quantity: 1, price: 49.99 }
    ],
    status: 'processing',
    createdAt: '2025-03-20T08:30:00Z'
  },
  {
    id: 'ord-002',
    customerId: 'cust-17',
    items: [
      { productId: 'prod-310', quantity: 3, price: 9.99 }
    ],
    status: 'shipped',
    createdAt: '2025-03-21T14:15:00Z'
  }
];

ordersRouter.get('/', (_req: Request, res: Response) => {
  res.status(200).json(orders);
});

ordersRouter.get('/:id', (req: Request, res: Response) => {
  const order = orders.find(o => o.id === req.params.id);
  if (!order) {
    res.status(404).json({ error: 'Order not found' });
    return;
  }
  res.status(200).json(order);
});
