import { useState, useEffect } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { Box, Card, MenuItem, Select, TextField, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import dayjs from "dayjs";
import axios from "axios";

export default function DeliveryReport() {
  const [dateFrom, setDateFrom] = useState(dayjs().subtract(7, "day").format("YYYY-MM-DD"));
  const [dateTo, setDateTo] = useState(dayjs().format("YYYY-MM-DD"));
  const [serviceFilter, setServiceFilter] = useState("");
  const [tableData, setTableData] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const token = localStorage.getItem("authToken");
        const res = await axios.get("/api/services/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        setServices(res.data);
      } catch (error) {
        if (error.response.status === 401) {
          localStorage.removeItem("authToken");
          window.location.reload();
        }
        console.error("Error fetching services:", error);
      }
    };
    fetchServices();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("authToken");
        const params = {
          arrival_time_from: dateFrom,
          arrival_time_to: dateTo,
        };
        if (serviceFilter) {
          params.service = serviceFilter;
        }
        const res = await axios.get("/api/deliveries/", {
          headers: {
            Authorization: `Token ${token}`,
          },
          params: params,
        });

        const newTableData = res.data.map((item) => ({
          id: item.id,
          date: dayjs(item.arrival_time).format("YYYY-MM-DD"),
          services: item.services || [],
          cargo: item.cargo || "Обычный",
          vehicle: item.transport_number,
          distance: item.distance_km,
        }));
        setTableData(newTableData);

        const dateCountMap = new Map();
        for (const delivery of newTableData) {
          const date = delivery.date;
          dateCountMap.set(date, (dateCountMap.get(date) || 0) + 1);
        }
        const groupedChart = Array.from(dateCountMap.entries()).map(([date, count]) => ({
          date,
          count,
        }));
        setChartData(groupedChart.sort((a, b) => a.date.localeCompare(b.date)));
      } catch (error) {
        if (error.response.status === 401) {
          localStorage.removeItem("authToken");
          window.location.reload();
        }
        console.error("Ошибка при загрузке доставок:", error);
      }
    };

    fetchData();
  }, [dateFrom, dateTo, serviceFilter]);

  return (
    <Box p={4}>
      <Typography variant="h5" gutterBottom>
        Отчет по доставкам
      </Typography>

      <Box display="flex" gap={2} mb={3}>
        <TextField
          type="date"
          label="С"
          value={dateFrom}
          onChange={(e) => setDateFrom(e.target.value)}
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />
        <TextField
          type="date"
          label="По"
          value={dateTo}
          onChange={(e) => setDateTo(e.target.value)}
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />
        <Select value={serviceFilter} onChange={(e) => setServiceFilter(e.target.value)} displayEmpty>
          <MenuItem value="">Все услуги</MenuItem>
          {services.map((service) => (
            <MenuItem key={service.id} value={service.id}>
              {service.name}
            </MenuItem>
          ))}
        </Select>
      </Box>

      <Card>
        <Box p={2}>
          <Typography variant="subtitle1">Количество доставок</Typography>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="color" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#1976d2" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#1976d2" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="count" stroke="#1976d2" fill="url(#color)" />
            </AreaChart>
          </ResponsiveContainer>
        </Box>
      </Card>
      <TableContainer component={Paper} sx={{ mt: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Итого</TableCell>
              <TableCell>Дата доставки</TableCell>
              <TableCell>Модель ТС</TableCell>
              <TableCell>Услуги</TableCell>
              <TableCell>Дистанция (км)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>Доставка {index + 1}</TableCell>
                <TableCell>{row.date}</TableCell>
                <TableCell>{row.vehicle ?? `A ${100 + index} AA`}</TableCell>
                <TableCell>
                  {row.services.length > 0 ? (
                    row.services.map((s, i) => (
                      <Typography key={i} variant="body2">
                        {s.name}
                      </Typography>
                    ))
                  ) : (
                    <Typography variant="body2" color="textSecondary">
                      Без услуги
                    </Typography>
                  )}
                </TableCell>
                <TableCell>{row.distance ?? 150 + index * 5}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
