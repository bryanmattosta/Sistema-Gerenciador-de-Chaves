-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/08/2026 às 02:42
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

--
-- Despejando dados para a tabela `tb_ambiente`
--

INSERT INTO `tb_ambiente` (`id_ambiente`, `ambiente`, `disponivel_ambiente`, `observacao_ambiente`) VALUES
(1, 'informatica1', 0, NULL);

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
  `disponivel` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `tb_chave`
--

INSERT INTO `tb_chave` (`id_chave`, `id_ambiente`, `nome_chave`, `identificador`, `observacao`, `disponivel`) VALUES
(1, 1, 'informatica1', 'rosa', NULL, '0');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_devolucao`
--

CREATE TABLE `tb_devolucao` (
  `id_devolucao` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `data_devolucao` date DEFAULT NULL,
  `hora_fim_devolucao` time DEFAULT NULL,
  `hora_inicio_devolucao` time DEFAULT NULL,
  `observacao_devoluca` varchar(250) DEFAULT NULL,
  `id_perfil` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tb_devolucao`
--

INSERT INTO `tb_devolucao` (`id_devolucao`, `id_reserva`, `data_devolucao`, `hora_fim_devolucao`, `hora_inicio_devolucao`, `observacao_devoluca`, `id_perfil`) VALUES
(1, 1, '2026-08-20', '21:40:00', '20:40:00', NULL, 0);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_movimentacao`
--

CREATE TABLE `tb_movimentacao` (
  `id_movimentacao` int(11) NOT NULL,
  `id_chave` int(11) DEFAULT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `id_ambiente` int(11) DEFAULT NULL,
  `data_movimentacao` date DEFAULT NULL,
  `hora_inicio_movimentacao` time DEFAULT NULL,
  `hora_fim_movimentacao` time DEFAULT NULL,
  `concluido` varchar(45) DEFAULT NULL,
  `id_reserva` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `tb_movimentacao`
--

INSERT INTO `tb_movimentacao` (`id_movimentacao`, `id_chave`, `id_perfil`, `id_ambiente`, `data_movimentacao`, `hora_inicio_movimentacao`, `hora_fim_movimentacao`, `concluido`, `id_reserva`) VALUES
(1, 1, 0, 1, '2026-08-20', NULL, NULL, NULL, NULL),
(2, 1, 0, 1, '2026-08-21', '20:40:00', '21:40:00', NULL, NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_movimentacao_devolucao`
--

CREATE TABLE `tb_movimentacao_devolucao` (
  `id_devolucao` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `date_reserva` date DEFAULT NULL,
  `horario_devolucao` time DEFAULT NULL,
  `obsevacao_devolucao` varchar(250) DEFAULT NULL
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

--
-- Despejando dados para a tabela `tb_perfil`
--

INSERT INTO `tb_perfil` (`id_perfil`, `nome_perfil`, `matricula`, `cargo`) VALUES
(0, 'Joao', 458745, 'Professor');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `tb_reserva`
--

INSERT INTO `tb_reserva` (`id_reserva`, `id_chave`, `id_ambiente`, `id_perfil`, `data_reserva`, `hora_inicio_reserva`, `hora_fim_reserva`) VALUES
(1, 1, 1, 0, '2026-08-20', '20:40:00', '21:40:00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_usuario`
--

CREATE TABLE `tb_usuario` (
  `id_usuario` int(11) NOT NULL,
  `nome_usuario` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `senha` decimal(15,0) NOT NULL,
  `id_perfil` int(11) DEFAULT NULL,
  `disponivel` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Despejando dados para a tabela `tb_usuario`
--

INSERT INTO `tb_usuario` (`id_usuario`, `nome_usuario`, `email`, `senha`, `id_perfil`, `disponivel`) VALUES
(0, 'Jose', 'jose@gmail.com', 1234, 0, NULL);

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
  ADD PRIMARY KEY (`id_devolucao`),
  ADD KEY `id_reserva` (`id_reserva`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- Índices de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  ADD PRIMARY KEY (`id_movimentacao`),
  ADD KEY `id_chave` (`id_chave`),
  ADD KEY `tb_movimentacao_ibfk_2` (`id_perfil`),
  ADD KEY `id_ambiente` (`id_ambiente`),
  ADD KEY `id_reserva` (`id_reserva`);

--
-- Índices de tabela `tb_movimentacao_devolucao`
--
ALTER TABLE `tb_movimentacao_devolucao`
  ADD PRIMARY KEY (`id_devolucao`);

--
-- Índices de tabela `tb_perfil`
--
ALTER TABLE `tb_perfil`
  ADD PRIMARY KEY (`id_perfil`);

--
-- Índices de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `id_chave` (`id_chave`),
  ADD KEY `id_ambiente` (`id_ambiente`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- Índices de tabela `tb_usuario`
--
ALTER TABLE `tb_usuario`
  ADD KEY `id_perfil` (`id_perfil`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tb_devolucao`
--
ALTER TABLE `tb_devolucao`
  MODIFY `id_devolucao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  MODIFY `id_movimentacao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `tb_movimentacao_devolucao`
--
ALTER TABLE `tb_movimentacao_devolucao`
  MODIFY `id_devolucao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_reserva`
--
ALTER TABLE `tb_reserva`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `tb_chave`
--
ALTER TABLE `tb_chave`
  ADD CONSTRAINT `tb_chave_ibfk_1` FOREIGN KEY (`id_ambiente`) REFERENCES `tb_ambiente` (`id_ambiente`);

--
-- Restrições para tabelas `tb_devolucao`
--
ALTER TABLE `tb_devolucao`
  ADD CONSTRAINT `tb_devolucao_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `tb_reserva` (`id_reserva`),
  ADD CONSTRAINT `tb_devolucao_ibfk_2` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`);

--
-- Restrições para tabelas `tb_movimentacao`
--
ALTER TABLE `tb_movimentacao`
  ADD CONSTRAINT `tb_movimentacao_ibfk_1` FOREIGN KEY (`id_chave`) REFERENCES `tb_chave` (`id_chave`),
  ADD CONSTRAINT `tb_movimentacao_ibfk_2` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`),
  ADD CONSTRAINT `tb_movimentacao_ibfk_3` FOREIGN KEY (`id_ambiente`) REFERENCES `tb_ambiente` (`id_ambiente`),
  ADD CONSTRAINT `tb_movimentacao_ibfk_4` FOREIGN KEY (`id_reserva`) REFERENCES `tb_reserva` (`id_reserva`);

--
-- Restrições para tabelas `tb_reserva`
--
ALTER TABLE `tb_reserva`
  ADD CONSTRAINT `tb_reserva_ibfk_1` FOREIGN KEY (`id_chave`) REFERENCES `tb_chave` (`id_chave`),
  ADD CONSTRAINT `tb_reserva_ibfk_2` FOREIGN KEY (`id_ambiente`) REFERENCES `tb_ambiente` (`id_ambiente`),
  ADD CONSTRAINT `tb_reserva_ibfk_3` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`);

--
-- Restrições para tabelas `tb_usuario`
--
ALTER TABLE `tb_usuario`
  ADD CONSTRAINT `tb_usuario_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `tb_perfil` (`id_perfil`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
