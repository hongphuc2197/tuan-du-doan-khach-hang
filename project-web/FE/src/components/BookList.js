import React from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Grid,
  Box,
  Chip,
  Button,
} from '@mui/material';

const books = [
  {
    id: 1,
    title: "Các Công Cụ AI Dành Cho Giáo Viên",
    author: "NXB Đại Học Sư Phạm",
    category: "Công nghệ giáo dục",
    description: "Cuốn sách giới thiệu các công cụ AI hiện đại giúp giáo viên nâng cao hiệu quả giảng dạy và quản lý lớp học.",
    image: "https://images.nxbdsh.vn/Picture/2024/5/11/image-20240511160935459.png",
    price: "150.000 VNĐ",
    publishYear: 2024,
    pages: 280,
    isbn: "978-604-123-456-7"
  },
  {
    id: 2,
    title: "Hướng Dẫn Giáo Viên Sử Dụng Các Công Cụ AI Trong Hoạt Động Dạy Học",
    author: "NXB Đại Học Sư Phạm",
    category: "Phương pháp giảng dạy",
    description: "Hướng dẫn chi tiết cách tích hợp AI vào quy trình dạy học, từ lập kế hoạch đến đánh giá kết quả.",
    image: "https://images.nxbdsh.vn/Picture/2024/10/4/image-20241004163927969.png",
    price: "180.000 VNĐ",
    publishYear: 2024,
    pages: 320,
    isbn: "978-604-123-457-4"
  },
  {
    id: 3,
    title: "Công Nghệ Phần Mềm",
    author: "NXB Đại Học Sư Phạm",
    category: "Công nghệ thông tin",
    description: "Giáo trình cơ bản về quy trình phát triển phần mềm, từ phân tích yêu cầu đến triển khai và bảo trì.",
    image: "https://images.nxbdsh.vn/Picture/2023/3/31/image-20230331100509876.png",
    price: "120.000 VNĐ",
    publishYear: 2023,
    pages: 250,
    isbn: "978-604-123-458-1"
  },
  {
    id: 4,
    title: "Bài Tập Thiết Kế Web",
    author: "NXB Đại Học Sư Phạm",
    category: "Thiết kế web",
    description: "Tuyển tập bài tập thực hành thiết kế web responsive, sử dụng HTML5, CSS3 và JavaScript hiện đại.",
    image: "https://images.nxbdsh.vn/Picture/2024/12/19/image-20241219154327988.png",
    price: "95.000 VNĐ",
    publishYear: 2024,
    pages: 200,
    isbn: "978-604-123-459-8"
  },
  {
    id: 5,
    title: "Cấu Trúc Dữ Liệu",
    author: "NXB Đại Học Sư Phạm",
    category: "Lập trình",
    description: "Giáo trình về các cấu trúc dữ liệu cơ bản và nâng cao, thuật toán xử lý và ứng dụng thực tế.",
    image: "https://images.nxbdsh.vn/Picture/2023/3/31/image-20230331100747118.png",
    price: "110.000 VNĐ",
    publishYear: 2023,
    pages: 280,
    isbn: "978-604-123-460-4"
  },
  {
    id: 6,
    title: "Phương Pháp Luận Nghiên Cứu Khoa Học",
    author: "NXB Đại Học Sư Phạm",
    category: "Nghiên cứu khoa học",
    description: "Hướng dẫn phương pháp nghiên cứu khoa học, từ xác định vấn đề đến viết báo cáo và thuyết trình.",
    image: "https://images.nxbdsh.vn/Picture/2024/10/23/image-20241023192253777.jpg",
    price: "140.000 VNĐ",
    publishYear: 2024,
    pages: 300,
    isbn: "978-604-123-461-1"
  },
  {
    id: 7,
    title: "Giáo Dục STEM Robotics Ở Trường Trung Học",
    author: "NXB Đại Học Sư Phạm",
    category: "Giáo dục STEM",
    description: "Phương pháp tích hợp STEM và Robotics vào chương trình giảng dạy trung học, kèm theo các dự án thực hành.",
    image: "https://images.nxbdsh.vn/Thumbs/2025/2/27/image-20250227185237079.jpg",
    price: "160.000 VNĐ",
    publishYear: 2024,
    pages: 350,
    isbn: "978-604-123-462-8"
  },
  {
    id: 8,
    title: "Hội Thảo Khoa Học Quốc Tế VNZ-TESOL Lần 3 Năm 2023",
    author: "NXB Đại Học Sư Phạm",
    category: "Giảng dạy tiếng Anh",
    description: "Kỷ yếu hội thảo về xây dựng cộng đồng học tập trong lĩnh vực giảng dạy tiếng Anh với các bài báo khoa học chất lượng.",
    image: "https://images.nxbdsh.vn/Picture/2024/3/22/image-20240322154922381.jpg",
    price: "200.000 VNĐ",
    publishYear: 2023,
    pages: 400,
    isbn: "978-604-123-463-5"
  },
  {
    id: 9,
    title: "Lập Trình Python Cho Người Mới Bắt Đầu",
    author: "NXB Đại Học Sư Phạm",
    category: "Lập trình",
    description: "Giáo trình Python cơ bản đến nâng cao, phù hợp cho người mới học lập trình với nhiều ví dụ thực tế.",
    image: "https://images.nxbdsh.vn/Thumbs/2024/4/17/image-20240417094052656.jpg",
    price: "130.000 VNĐ",
    publishYear: 2024,
    pages: 320,
    isbn: "978-604-123-464-2"
  },
  {
    id: 10,
    title: "Thiết Kế Giao Diện Người Dùng (UI/UX)",
    author: "NXB Đại Học Sư Phạm",
    category: "Thiết kế",
    description: "Nguyên tắc thiết kế UI/UX hiện đại, các công cụ thiết kế và phương pháp tạo trải nghiệm người dùng tốt nhất.",
    image: "https://down-vn.img.susercontent.com/file/vn-11134207-7r98o-luefgockttzlf1.webp",
    price: "170.000 VNĐ",
    publishYear: 2024,
    pages: 280,
    isbn: "978-604-123-465-9"
  },
  {
    id: 11,
    title: "Cơ Sở Dữ Liệu Và Hệ Quản Trị Cơ Sở Dữ Liệu",
    author: "NXB Đại Học Sư Phạm",
    category: "Cơ sở dữ liệu",
    description: "Giáo trình về thiết kế cơ sở dữ liệu, SQL và các hệ quản trị cơ sở dữ liệu phổ biến như MySQL, PostgreSQL.",
    image: "https://vietbooks.info/attachments/upload_2022-12-10_16-55-17-png.18127/",
    price: "145.000 VNĐ",
    publishYear: 2023,
    pages: 300,
    isbn: "978-604-123-466-6"
  },
  {
    id: 12,
    title: "Phát Triển Ứng Dụng Di Động Với React Native",
    author: "NXB Đại Học Sư Phạm",
    category: "Phát triển ứng dụng",
    description: "Hướng dẫn xây dựng ứng dụng di động đa nền tảng sử dụng React Native, từ cơ bản đến nâng cao.",
    image: "https://images.nxbdsh.vn/Thumbs/2024/4/17/image-20240417094052656.jpg",
    price: "190.000 VNĐ",
    publishYear: 2024,
    pages: 380,
    isbn: "978-604-123-467-3"
  }
];

const categories = [
  "Tất cả",
  "Công nghệ giáo dục",
  "Phương pháp giảng dạy",
  "Công nghệ thông tin",
  "Thiết kế web",
  "Lập trình",
  "Nghiên cứu khoa học",
  "Giáo dục STEM",
  "Giảng dạy tiếng Anh",
  "Thiết kế",
  "Cơ sở dữ liệu",
  "Phát triển ứng dụng"
];

const BookList = () => {
  const [selectedCategory, setSelectedCategory] = React.useState("Tất cả");

  const filteredBooks = selectedCategory === "Tất cả" 
    ? books 
    : books.filter(book => book.category === selectedCategory);

  const getCategoryColor = (category) => {
    const colors = {
      "Công nghệ giáo dục": "#4CAF50",
      "Phương pháp giảng dạy": "#2196F3",
      "Công nghệ thông tin": "#FF9800",
      "Thiết kế web": "#9C27B0",
      "Lập trình": "#F44336",
      "Nghiên cứu khoa học": "#795548",
      "Giáo dục STEM": "#607D8B",
      "Giảng dạy tiếng Anh": "#E91E63",
      "Thiết kế": "#00BCD4",
      "Cơ sở dữ liệu": "#8BC34A",
      "Phát triển ứng dụng": "#FF5722"
    };
    return colors[category] || "#757575";
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Danh mục sách công nghệ giáo dục
      </Typography>
      
      {/* Filter buttons */}
      <Box sx={{ mb: 3, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {categories.map((category) => (
          <Chip
            key={category}
            label={category}
            onClick={() => setSelectedCategory(category)}
            color={selectedCategory === category ? "primary" : "default"}
            variant={selectedCategory === category ? "filled" : "outlined"}
          />
        ))}
      </Box>

      {/* Books grid */}
      <Grid container spacing={3}>
        {filteredBooks.map((book) => (
          <Grid item xs={12} sm={6} md={4} key={book.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="200"
                image={book.image}
                alt={book.title}
                sx={{ objectFit: 'cover' }}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2" noWrap>
                  {book.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {book.author}
                </Typography>
                <Chip
                  label={book.category}
                  size="small"
                  sx={{
                    backgroundColor: getCategoryColor(book.category),
                    color: 'white',
                    mb: 1
                  }}
                />
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {book.description.length > 100 
                    ? `${book.description.substring(0, 100)}...` 
                    : book.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                  <Typography variant="h6" color="primary">
                    {book.price}
                  </Typography>
                  <Button variant="contained" size="small">
                    Xem chi tiết
                  </Button>
                </Box>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  {book.pages} trang • {book.publishYear} • ISBN: {book.isbn}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default BookList;