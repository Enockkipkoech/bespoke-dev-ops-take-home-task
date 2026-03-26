import express, { Request, Response } from 'express';
import { ordersRouter } from './routes/orders';
import { requestLogger } from './middleware/logger';

const app = express();
const PORT = Number(process.env.PORT) || 3000;

app.use(express.json());
app.use(requestLogger);

app.get('/healthz', (_req: Request, res: Response) => {
  res.status(200).json({ status: 'ok' });
});

app.use('/api/orders', ordersRouter);

app.listen(PORT, () => {
  console.log(`order-service listening on port ${PORT}`);
});

export default app;
