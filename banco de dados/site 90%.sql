-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 24/08/2026 às 23:03
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
(2, 'Informática 1', 'Sala', '1 andar', 1, '30 computadores');

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
(2, 2, 'Informática', 'azul', 1);

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
(2, 2, 2, '436221', '2026-08-25 17:41:00', '2026-08-24 17:50:20', '2026-08-24 17:54:42', 'Devolvido', '2026-08-25 18:41:00');

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
(2, 'Joao', '4214512', 'Professor', 1);

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
  `senha_usuario` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_usuario`
--

INSERT INTO `tb_usuario` (`id_usuario`, `id_perfil`, `email`, `senha_usuario`) VALUES
(2, 2, 'joao@gmail.com', '1234');

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
  MODIFY `id_ambiente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tb_chave`
--
ALTER TABLE `tb_chave`
  MODIFY `id_chave` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tb_devolucao`
--
ALTER TABLE `tb_devolucao`
  MODIFY `id_devolucao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  MODIFY `id_movimentacao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  MODIFY `id_perfil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
