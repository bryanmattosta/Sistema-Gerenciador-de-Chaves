-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 25/08/2026 às 22:11
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `db_chave`
--
CREATE DATABASE IF NOT EXISTS `db_chave` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `db_chave`;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_ambiente`
--

CREATE TABLE `tb_ambiente` (
  `id_ambiente` int(11) NOT NULL,
  `nome_sala` varchar(150) DEFAULT NULL,
  `tipo` varchar(150) DEFAULT NULL,
  `localizacao` varchar(250) DEFAULT NULL,
  `status_ambiente` tinyint(4) DEFAULT NULL,
  `observacao_ambiente` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_ambiente`
--

INSERT INTO `tb_ambiente` (`id_ambiente`, `nome_sala`, `tipo`, `localizacao`, `status_ambiente`, `observacao_ambiente`) VALUES
(2, 'Informática 1', 'Sala', '1 andar', 1, '30 computadores'),
(3, 'Laboratório ', 'Sala', '1 andar', 1, '30');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_chave`
--

CREATE TABLE `tb_chave` (
  `id_chave` int(11) NOT NULL,
  `id_ambiente` int(11) DEFAULT NULL,
  `nome_chave` varchar(150) DEFAULT NULL,
  `observacao_chave` varchar(250) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_chave`
--

INSERT INTO `tb_chave` (`id_chave`, `id_ambiente`, `nome_chave`, `observacao_chave`, `status`) VALUES
(2, 2, 'Informática', 'azul', 1),
(3, 3, 'Laboratório', 'roxo', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_devolucao`
--

CREATE TABLE `tb_devolucao` (
  `id_devolucao` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `data_devolucao` date DEFAULT NULL,
  `hora_fim_devolucao` time DEFAULT NULL,
  `hora_inicio_devolucao` time DEFAULT NULL,
  `observacao_devoluca` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_movimentacao`
--

CREATE TABLE `tb_movimentacao` (
  `id_movimentacao` int(11) NOT NULL,
  `id_chave` int(11) DEFAULT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `codigo_reserva` varchar(250) DEFAULT NULL,
  `date_hora_reserva` datetime DEFAULT NULL,
  `date_hora_retirada` datetime DEFAULT NULL,
  `date_hora_devolucao` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date_hora_devolucao_prev` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_movimentacao`
--

INSERT INTO `tb_movimentacao` (`id_movimentacao`, `id_chave`, `id_perfil`, `codigo_reserva`, `date_hora_reserva`, `date_hora_retirada`, `date_hora_devolucao`, `status`, `date_hora_devolucao_prev`) VALUES
(2, 2, 2, '436221', '2026-08-25 17:41:00', '2026-08-24 17:50:20', '2026-08-24 17:54:42', 'Devolvido', '2026-08-25 18:41:00'),
(3, 2, 3, '871525', '2026-08-28 20:28:00', '2026-08-25 17:02:24', '2026-08-25 17:02:38', 'Devolvido', '2026-08-28 21:29:00'),
(4, 2, 3, '830600', '2026-08-26 21:40:00', NULL, NULL, 'Reservado', '2026-08-25 22:42:00'),
(5, 2, 3, '657309', '2026-08-26 16:43:00', NULL, NULL, 'Reservado', '2026-08-26 18:43:00'),
(6, 3, 3, '119441', '2026-08-25 17:01:00', NULL, NULL, 'Reservado', '2026-08-25 18:01:00'),
(7, 3, 3, '989617', '2026-08-25 17:01:00', NULL, NULL, 'Reservado', '2026-08-25 19:01:00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_perfil`
--

CREATE TABLE `tb_perfil` (
  `id_perfil` int(11) NOT NULL,
  `nome_perfil` varchar(250) DEFAULT NULL,
  `matricula` varchar(250) DEFAULT NULL,
  `cargo` varchar(200) DEFAULT NULL,
  `status_perfil` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_perfil`
--

INSERT INTO `tb_perfil` (`id_perfil`, `nome_perfil`, `matricula`, `cargo`, `status_perfil`) VALUES
(2, 'Joao', '4214512', 'Professor', 1),
(3, 'bryan', '454215545', 'Administrador', 1),
(4, 'Edy', '32345242', 'Professor', 1),
(5, 'Gabriel', '132324', 'Atendente', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_reserva`
--

CREATE TABLE `tb_reserva` (
  `id_reserva` int(11) NOT NULL,
  `id_chave` int(11) DEFAULT NULL,
  `id_ambiente` int(11) DEFAULT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `data_reserva` date DEFAULT NULL,
  `hora_inicio_reserva` time DEFAULT NULL,
  `hora_fim_reserva` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_usuario`
--

CREATE TABLE `tb_usuario` (
  `id_usuario` int(11) NOT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `senha_usuario` varchar(250) DEFAULT NULL,
  `nivel` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_usuario`
--

INSERT INTO `tb_usuario` (`id_usuario`, `id_perfil`, `email`, `senha_usuario`, `nivel`) VALUES
(2, 2, 'joao@gmail.com', '1234', NULL),
(3, 3, 'mattosbryan10@gmail.com', 'scrypt:32768:8:1$Sk4Yp21RSbG77ebu$e7af3ccf9e5731b77cfd0152543be5fd5d8587aecd65e3197c2265b900aa7e35a11756200fde7100c62c42340708c6f17bc46b1b4696ae62d3a4a7971b68beda', 'Administrador'),
(4, 4, 'Edy@gmail.com', 'scrypt:32768:8:1$Hty1Bfxhc98QXXDc$5400472a6782855134085db23b919ef1361b0c617d5a95da765bebbeedf7907da72665edd8529de398becab1a2a1aa0a815d8dc59b40d50883cd01fe94d989e5', 'Professor'),
(5, 5, 'Gabriel@gmail.com', 'scrypt:32768:8:1$nphGAuXlRUWPXRDb$08268d5a825f9d0d9b82340eec84fe35d0984f0b4d08c155bd45354ac4a219d0a68f7ed648f6a9ab121dbb9f7483880e7b12fea37b069efd38cfa9e24c7ae01e', 'Atendente');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `tb_ambiente`
--
ALTER TABLE `tb_ambiente`
  ADD PRIMARY KEY (`id_ambiente`);

--
-- Índices de tabela `tb_chave`
--
ALTER TABLE `tb_chave`
  ADD PRIMARY KEY (`id_chave`),
  ADD KEY `id_ambiente` (`id_ambiente`);

--
-- Índices de tabela `tb_devolucao`
--
ALTER TABLE `tb_devolucao`
  ADD PRIMARY KEY (`id_devolucao`);

--
-- Índices de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  ADD PRIMARY KEY (`id_movimentacao`),
  ADD KEY `id_chave` (`id_chave`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- Índices de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  ADD PRIMARY KEY (`id_perfil`);

--
-- Índices de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  ADD PRIMARY KEY (`id_reserva`);

--
-- Índices de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tb_ambiente`
--
ALTER TABLE `tb_ambiente`
  MODIFY `id_ambiente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `tb_chave`
--
ALTER TABLE `tb_chave`
  MODIFY `id_chave` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `tb_devolucao`
--
ALTER TABLE `tb_devolucao`
  MODIFY `id_devolucao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  MODIFY `id_movimentacao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  MODIFY `id_perfil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `tb_chave`
--
ALTER TABLE `tb_chave`
  ADD CONSTRAINT `tb_chave_ibfk_1` FOREIGN KEY (`id_ambiente`) REFERENCES `tb_ambiente` (`id_ambiente`);

--
-- Restrições para tabelas `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  ADD CONSTRAINT `tb_movimentacao_ibfk_1` FOREIGN KEY (`id_chave`) REFERENCES `tb_chave` (`id_chave`),
  ADD CONSTRAINT `tb_movimentacao_ibfk_2` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`);

--
-- Restrições para tabelas `tb_usuario`
--
ALTER TABLE `tb_usuario`
  ADD CONSTRAINT `tb_usuario_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
