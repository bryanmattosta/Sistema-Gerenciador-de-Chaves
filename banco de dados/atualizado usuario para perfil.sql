-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 15/08/2026 às 01:34
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

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
  `ambiente` varchar(150) NOT NULL,
  `disponivel_ambiente` tinyint(4) NOT NULL,
  `observacao_ambiente` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_chave`
--

CREATE TABLE `tb_chave` (
  `id_chave` int(11) NOT NULL,
  `id_ambiente` int(11) DEFAULT NULL,
  `nome_chave` varchar(250) DEFAULT NULL,
  `identificador` varchar(250) DEFAULT NULL,
  `observacao` varchar(250) DEFAULT NULL,
  `disponivel` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_movimentacao`
--

CREATE TABLE `tb_movimentacao` (
  `id_movimentacao` int(11) NOT NULL,
  `id_chave` int(11) DEFAULT NULL,
  `id_pessoa` int(11) DEFAULT NULL,
  `data_retirada` date DEFAULT NULL,
  `horario_inicio` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_movimentacao_devolucao`
--

CREATE TABLE `tb_movimentacao_devolucao` (
  `id_devolucao` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `date_devolucao` date DEFAULT NULL,
  `horario_devolucao` time DEFAULT NULL,
  `observacao_devolucao` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_perfil`
--

CREATE TABLE `tb_perfil` (
  `id_perfil` int(11) NOT NULL,
  `nome_perfil` varchar(200) NOT NULL,
  `matricula` decimal(12,0) NOT NULL,
  `cargo` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_pessoa`
--

CREATE TABLE `tb_pessoa` (
  `id_pessoa` int(11) NOT NULL,
  `nome_pessoa` varchar(200) DEFAULT NULL,
  `matricula` decimal(12,0) DEFAULT NULL,
  `cargo` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_reserva`
--

CREATE TABLE `tb_reserva` (
  `id_reserva` int(11) NOT NULL,
  `id_chave` int(11) DEFAULT NULL,
  `id_ambiente` int(11) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `data_reserva` date DEFAULT NULL,
  `horario_reserva` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_usuario`
--

CREATE TABLE `tb_usuario` (
  `id_usuario` int(11) NOT NULL,
  `nome_usuario` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `senha` decimal(15,0) NOT NULL,
  `perfil` varchar(150) DEFAULT NULL,
  `disponivel` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
-- Índices de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  ADD PRIMARY KEY (`id_movimentacao`),
  ADD KEY `id_chave` (`id_chave`),
  ADD KEY `id_pessoa` (`id_pessoa`);

--
-- Índices de tabela `tb_movimentacao_devolucao`
--
ALTER TABLE `tb_movimentacao_devolucao`
  ADD PRIMARY KEY (`id_devolucao`),
  ADD KEY `id_reserva` (`id_reserva`);

--
-- Índices de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  ADD PRIMARY KEY (`id_perfil`);

--
-- Índices de tabela `tb_pessoa`
--
ALTER TABLE `tb_pessoa`
  ADD PRIMARY KEY (`id_pessoa`);

--
-- Índices de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `id_chave` (`id_chave`),
  ADD KEY `id_ambiente` (`id_ambiente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Índices de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tb_ambiente`
--
ALTER TABLE `tb_ambiente`
  MODIFY `id_ambiente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_chave`
--
ALTER TABLE `tb_chave`
  MODIFY `id_chave` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  MODIFY `id_movimentacao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao_devolucao`
--
ALTER TABLE `tb_movimentacao_devolucao`
  MODIFY `id_devolucao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  MODIFY `id_perfil` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_pessoa`
--
ALTER TABLE `tb_pessoa`
  MODIFY `id_pessoa` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

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
  ADD CONSTRAINT `tb_movimentacao_ibfk_2` FOREIGN KEY (`id_pessoa`) REFERENCES `tb_perfil` (`id_perfil`);

--
-- Restrições para tabelas `tb_movimentacao_devolucao`
--
ALTER TABLE `tb_movimentacao_devolucao`
  ADD CONSTRAINT `tb_movimentacao_devolucao_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `tb_reserva` (`id_reserva`);

--
-- Restrições para tabelas `tb_reserva`
--
ALTER TABLE `tb_reserva`
  ADD CONSTRAINT `tb_reserva_ibfk_1` FOREIGN KEY (`id_chave`) REFERENCES `tb_chave` (`id_chave`),
  ADD CONSTRAINT `tb_reserva_ibfk_2` FOREIGN KEY (`id_ambiente`) REFERENCES `tb_ambiente` (`id_ambiente`),
  ADD CONSTRAINT `tb_reserva_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
