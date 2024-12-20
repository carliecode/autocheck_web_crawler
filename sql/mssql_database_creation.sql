USE [autocheck_db]
GO
/****** Object:  Schema [silver]    Script Date: 11/19/2024 11:36:46 PM ******/
CREATE SCHEMA [silver]
GO
/****** Object:  Table [silver].[car_prices]    Script Date: 11/19/2024 11:36:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [silver].[car_prices](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Manufacturer] [varchar](50) NULL,
	[Model] [varchar](50) NULL,
	[Year] [varchar](10) NULL,
	[Transmission] [varchar](50) NULL,
	[Color] [varchar](50) NULL,
	[Type] [varchar](50) NULL,
	[State] [varchar](50) NULL,
	[Area] [varchar](50) NULL,
	[Price] [decimal](18, 2) NULL,
	[Created_At] [datetime] NULL,
 CONSTRAINT [PK__cars_pri__3214EC07A0473792] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [silver].[car_prices] ADD  CONSTRAINT [DF_car_prices_Created_At]  DEFAULT (getdate()) FOR [Created_At]
GO
